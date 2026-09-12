# Documentation index

**Map of folders, not an inventory of files.** Per-artifact detail is kept where
it is actually maintained: see "Where per-artifact detail lives" below. This file
changes only when the structure changes.

## Entry points

| Document | What it is for |
|---|---|
| [`README.md`](README.md) | Project orientation: objective, main result, status, repository map |
| [`docs/fot_walkthrough_conversazione_studio2.md`](docs/fot_walkthrough_conversazione_studio2.md) | **Study 2 walkthrough.** Living document, updated phase by phase. A skeleton as of 2026-09-12: while a section is empty the authoritative source is the experiment plan |
| [`docs/letteratura.md`](docs/letteratura.md) | **The literature corpus.** Single active home, shared by every study. Numbering §14.1–§14.7 kept from its former place |
| [`docs/paper/FoT_TEP_Review_Piano_Sperimentale.md`](docs/paper/FoT_TEP_Review_Piano_Sperimentale.md) | **Study 2 design.** §§8–11 and §13; §0.1 lists what is not frozen yet |
| [`docs/fot_walkthrough_conversazione_v2.md`](docs/fot_walkthrough_conversazione_v2.md) | **First study: record.** Consultable, not cited in the new paper and not a source for study 2's design |
| [`AUDIT_GUIDE.md`](AUDIT_GUIDE.md) | Independent verification path for every frozen result |
| [`docs/MAINTENANCE.md`](docs/MAINTENANCE.md) | Maintenance contract: content categories, what is frozen, what must stay in sync |

## Folder map

| Folder | Holds | Rule |
|---|---|---|
| [`studio2/`](studio2) | Study 2 work, artifacts and macro-phase reports | Single operational root under `docs/MAINTENANCE.md` §8; experiment design remains in its authoritative documents |
| [`docs/`](docs) | Walkthrough documents and the literature corpus | Two studies, not two versions: `_studio2` is live, `_v2` and the unsuffixed pair are the first study's record. See `docs/MAINTENANCE.md` §3.1 |
| [`docs/paper/`](docs/paper) | Material for the future paper: blueprint and experiment plan | Not process documentation |
| [`docs/lit_review/`](docs/lit_review) | Supporting analyses and decision records for study 2 | Not a parallel corpus: the literature lives in `docs/letteratura.md` and nowhere else |
| [`docs/archive/`](docs/archive) | Closed snapshots of superseded documents | Read-only; each carries a header saying what migrated where |
| [`docs/audits/`](docs/audits) | Audits produced during the FoT-TEP process | Not audits of imported work |
| [`docs/figures/`](docs/figures) | Figures and their manifest | |
| [`docs/prompts/`](docs/prompts) | Operational handoff prompts | |
| [`papers/`](papers) | Literature papers: `.pdf` + `.md` + `_images/` | One copy per paper; `papers/README.md` carries what `ls` cannot say |
| [`papers/archive/`](papers/archive) | Dated snapshots imported from previous work | Not the current corpus; each has its own provenance README |
| [`papers/tools/`](papers/tools) | PDF-to-Markdown converter | Not literature |
| [`code/`](code) | Phase A pipeline: verbalizer, thresholds, tests | |
| [`phase_b/`](phase_b) | Phase B: protocol, insights, inference, evaluations, baselines, A+, C06 | **Frozen — never modify** |
| [`icl/`](icl) | Condition C, centralized pooled reference | **Frozen** |
| [`ablation/`](ablation) | Representation comparison | **Frozen** |
| [`analysis/`](analysis) | Communication payload characterization | |
| [`reproducibility/`](reproducibility) | Reproducibility records | |
| [`supporting_records/`](supporting_records) | Narratives, syntheses, provenance, superseded material | `supporting_records/historical/` holds Phase B design specs V1 and V2, both superseded by the frozen protocol; V1 (`PHASE_B_EXPERIMENT_DESIGN.md`) is local only and **not git-tracked**, so it is deliberately not linked |
| `tep_validation_v2/`, `tep_test_v2/`, `tep_cache/`, `dataset_pv/`, `swat/` | Data, caches, datasets | Largely git-ignored |

## Where per-artifact detail lives

| Question | Go to |
|---|---|
| Which artifact backs a given result, and how do I verify its bytes? | [`AUDIT_GUIDE.md`](AUDIT_GUIDE.md) §5 to §13 |
| Where is the artifact for a given section of the walkthrough? | Walkthrough, §15.2 "Dove si trova ogni cosa" |
| Which works were consulted, what do they forbid us to claim? | Walkthrough §14.1 to §14.7 — the only place |
| Which frozen tag anchors which milestone? | [`AUDIT_GUIDE.md`](AUDIT_GUIDE.md) §14 |
| What is in this folder and why? | The folder's own `README.md`, when it has one |

Condition A+, the C06 local-first mitigation and the C02B numerical baselines are
frozen by hash manifest and **carry no git tag**: see `AUDIT_GUIDE.md` §11 to §13.
