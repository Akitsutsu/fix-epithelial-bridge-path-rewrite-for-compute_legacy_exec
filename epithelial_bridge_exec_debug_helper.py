#!/usr/bin/env python3
"""Utilities to instrument compute_legacy exec bridges.

This module is designed for the Week 2 epithelial compute bridge where the
legacy source is rewritten in memory and then executed via ``exec()``.

Primary goals:
- persist the rewritten source before execution
- write adapter metadata *before* execution begins
- capture full tracebacks to a sidecar file if compile/exec fails
- update the adapter metadata on success or failure

The code is intentionally self-contained so it can be copied into a repo even
when the original bridge script is still in flux.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, MutableMapping
import datetime as dt
import hashlib
import json
import os
import traceback


JSONScalar = str | int | float | bool | None
JSONLike = JSONScalar | list["JSONLike"] | dict[str, "JSONLike"]


@dataclass(slots=True)
class ExecDebugPaths:
    """Filesystem targets for bridge debug artifacts."""

    stage_dir: Path
    query_id: str
    stage_name: str = "epithelial"
    adapter_meta_json: Path | None = None
    rewritten_script_py: Path | None = None
    traceback_txt: Path | None = None

    def __post_init__(self) -> None:
        self.stage_dir = Path(self.stage_dir)
        stem = f"{self.query_id}_{self.stage_name}"
        if self.adapter_meta_json is None:
            self.adapter_meta_json = self.stage_dir / f"{stem}_adapter_meta.json"
        if self.rewritten_script_py is None:
            self.rewritten_script_py = self.stage_dir / f"{stem}_rewritten_debug.py"
        if self.traceback_txt is None:
            self.traceback_txt = self.stage_dir / f"{stem}_traceback.txt"


@dataclass(slots=True)
class ExecDebugContext:
    """Context persisted into adapter metadata."""

    query_id: str
    stage_name: str = "epithelial"
    original_source_path: str | None = None
    query_h5ad: str | None = None
    reference_h5ad: str | None = None
    reference_meta: str | None = None
    whole_lung_gate_csv: str | None = None
    outdir: str | None = None
    replacements: dict[str, str] = field(default_factory=dict)
    extra: dict[str, JSONLike] = field(default_factory=dict)


def _utc_now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _atomic_write_text(path: Path, text: str, encoding: str = "utf-8") -> None:
    _ensure_parent(path)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding=encoding)
    os.replace(tmp, path)


def _atomic_write_json(path: Path, payload: Mapping[str, Any]) -> None:
    _atomic_write_text(path, json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def mark_exec_prepared(
    *,
    paths: ExecDebugPaths,
    context: ExecDebugContext,
    rewritten_source: str,
) -> dict[str, Any]:
    """Persist the rewritten source and a pre-exec metadata record.

    Returns the metadata dictionary written to disk so callers may reuse or
    enrich it if needed.
    """
    paths.stage_dir.mkdir(parents=True, exist_ok=True)

    _atomic_write_text(paths.rewritten_script_py, rewritten_source)

    meta: dict[str, Any] = {
        "query_id": context.query_id,
        "stage_name": context.stage_name,
        "status": "prepared",
        "prepared_at_utc": _utc_now_iso(),
        "original_source_path": context.original_source_path,
        "rewritten_debug_path": str(paths.rewritten_script_py),
        "traceback_path": str(paths.traceback_txt),
        "adapter_meta_path": str(paths.adapter_meta_json),
        "rewritten_source_sha256": sha256_text(rewritten_source),
        "rewritten_source_nchars": len(rewritten_source),
        "query_h5ad": context.query_h5ad,
        "reference_h5ad": context.reference_h5ad,
        "reference_meta": context.reference_meta,
        "whole_lung_gate_csv": context.whole_lung_gate_csv,
        "outdir": context.outdir,
        "replacements": context.replacements,
        "extra": context.extra,
    }
    _atomic_write_json(paths.adapter_meta_json, meta)
    return meta


def _write_failure(
    *,
    paths: ExecDebugPaths,
    meta: MutableMapping[str, Any],
    exc: BaseException,
) -> None:
    tb_text = traceback.format_exc()
    _atomic_write_text(paths.traceback_txt, tb_text)
    meta.update(
        {
            "status": "failed",
            "failed_at_utc": _utc_now_iso(),
            "exception_type": type(exc).__name__,
            "exception_message": str(exc),
            "traceback_path": str(paths.traceback_txt),
        }
    )
    _atomic_write_json(paths.adapter_meta_json, meta)


def _write_success(*, paths: ExecDebugPaths, meta: MutableMapping[str, Any]) -> None:
    meta.update(
        {
            "status": "ok",
            "completed_at_utc": _utc_now_iso(),
        }
    )
    _atomic_write_json(paths.adapter_meta_json, meta)


def run_compiled_rewritten_source(
    *,
    rewritten_source: str,
    paths: ExecDebugPaths,
    meta: MutableMapping[str, Any],
    exec_globals: MutableMapping[str, Any] | None = None,
    exec_locals: MutableMapping[str, Any] | None = None,
    filename: str | None = None,
) -> None:
    """Compile and execute the rewritten legacy source with debug persistence.

    The function re-raises any exception after writing the traceback and
    updating adapter metadata. This keeps the surrounding runner semantics
    unchanged while making the failure point observable.
    """
    if exec_globals is None:
        exec_globals = {}

    exec_globals.setdefault("__name__", "__main__")
    exec_globals.setdefault("__file__", filename or str(paths.rewritten_script_py))

    try:
        code = compile(rewritten_source, exec_globals["__file__"], "exec")
        exec(code, exec_globals, exec_locals)
    except BaseException as exc:  # noqa: BLE001 - preserve original failure semantics
        _write_failure(paths=paths, meta=meta, exc=exc)
        raise
    else:
        _write_success(paths=paths, meta=meta)


def load_adapter_meta(path: str | os.PathLike[str]) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


__all__ = [
    "ExecDebugContext",
    "ExecDebugPaths",
    "load_adapter_meta",
    "mark_exec_prepared",
    "run_compiled_rewritten_source",
    "sha256_text",
]
