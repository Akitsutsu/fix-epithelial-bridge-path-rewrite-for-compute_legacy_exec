# Tracked Cleanup Patch Summary v3

Date: 2026-04-03
Branch: `chore/repo_cleanup_v3` (from `main` at `35543c6`)

---

## Deleted tracked files (17)

### Development notes (5)
| File | Rationale |
|---|---|
| `compute_legacy_exec_bridge_note_v1.md` | Bridge development note; not referenced by any canonical doc |
| `next_step_runbook_CA1_BU3.md` | Runbook with all steps completed |
| `week1_manifest_runner_contract_v1.md` | v1 runner contract; superseded by v2 runner |
| `week1_replay_adapter_note.md` | Replay mode notes; approach abandoned in favor of compute_legacy_exec |
| `week2_compute_parity_playbook.md` | Compute parity playbook; parity achieved and verified |

### Debugging/example scripts (6)
| File | Rationale |
|---|---|
| `scan_rewritten_script_for_hardcodes.py` | One-shot debugging utility; unreferenced |
| `run_common_benchmark_example.sh` | Example shell script; v2 runner has own templates |
| `run_compute_legacy_example.sh` | Example shell script; superseded by v2 templates |
| `inspect_epi_bridge_failure.py` | Debugging helper for epithelial bridge; fix committed |
| `epithelial_bridge_exec_debug_helper.py` | Debugging helper; fix committed |
| `epithelial_only_remap_common_v2_integration_snippet.py` | Integration snippet; fully integrated into v2 adapter |

### v1 runner/adapter/template code (6)
| File | Rationale |
|---|---|
| `benchmark_common_runner_v1.py` | v1 runner; fully superseded by benchmark_common_runner_v2.py |
| `epithelial_only_remap_common_v1.py` | v1 epithelial adapter; superseded by v2 |
| `whole_lung_project_common_v1.py` | v1 whole-lung adapter; superseded by v2 |
| `epithelial_cmd_template_replay_v1.txt` | Replay-mode template; approach abandoned |
| `whole_lung_cmd_template_replay_v1.txt` | Replay-mode template; approach abandoned |
| `legacy_output_manifest_v1.example.csv` | Example manifest for replay mode; no longer needed |

## .gitignore changes

None in this commit (already up to date on main from prior merge).

## Rollback guidance

All deleted files are recoverable from git history:
```bash
git checkout 35543c6 -- <filename>
```

The parent commit `35543c6` (main at time of branch creation) contains all files.
