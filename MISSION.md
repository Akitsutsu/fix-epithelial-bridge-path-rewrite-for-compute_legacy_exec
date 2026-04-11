# claim-first OS toward a fetal lung–organoid digital twin

## Purpose
This repository is a lightweight research OS for linking fetal lung data and organoid data under a claim-first workflow.

It is designed to support:
- biologically interpretable fetal lung ↔ organoid alignment
- explicit claim tracking
- evidence registration at the sample / condition / paired-split level
- disciplined human review before strong biological statements

## Current focus
The near-term focus is not "collect more datasets" by default.
The near-term focus is to reduce uncertainty in a small number of biological questions by using the minimum necessary evidence.

Initial emphasis:
- fetal lung ↔ organoid alignment for alveolarization-related states
- disentangling format effects from directed biological effects
- building a usable operating system for claim-linked evidence review

## What this repo is
This repo is:
- a claim-first operating layer
- a biological interpretation layer
- a lightweight evidence registration layer

This repo is not:
- a raw-data warehouse
- a monolithic execution stack
- a cumulative summary repo that grows by default with each new dataset

## Boundary with the legacy repo
`Akitsutsu/fix-epithelial-bridge-path-rewrite-for-compute_legacy_exec` remains the legacy audit / evidence archive.

This repo is a new workspace.
It may inherit stable biological and reference assumptions from the legacy repo, but it does not inherit the full operational structure of that repo.

## Operating principle
The default unit of reasoning is not a dataset.
The default unit of reasoning is an evidence unit that can be linked to a biological question.

The system should prefer:
- biological interpretability over workflow expansion
- explicit uncertainty reduction over metadata accumulation
- stable contracts over prompt-only conventions

## Non-goals for v0.1
This repo does not aim to:
- rebuild the full legacy engineering stack
- mirror every old artifact
- formalize every possible biological program at the start
- automate final biological judgment

## Human / AI division
AI may help draft, register, summarize, and check consistency.

Humans retain final authority over:
- claim acceptance
- evidence admissibility
- hold / promote decisions
- interpretation of biological significance
