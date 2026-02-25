# α-KIV FBA Reproducible Project (COBRApy + BiGG)

This repository contains a reproducible Python workflow to analyse **α-ketoisovalerate (α-KIV / 3mob)** production from **lactate as sole carbon source in M9 medium** with **E. coli GEMs**.

## Highlights
- Default model: **iML1515**; optional comparator: **iJO1366**.
- Parallel feed scenarios: **L-lactate only** and **racemate (L/D)**.
- Process modes: **constant aerobic** vs **two-stage aerobic→microaerobic**.
- Native-first pathway validation, then literature-guided proxy scenarios.
- GLPK-first design search with documented fallback enumerative strategy.
- Outputs: tables, PNG figures, logs, manifests, and markdown report scaffolding.

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run_pipeline.py --model iML1515 --run all
```

## Resumability/checkpointing
Each experiment folder stores `summary.json`; pipeline-wide status is in:
- `results/manifests/pipeline_status.json`
- `results/manifests/run_manifest.json`

Rerun a single step:
```bash
python run_pipeline.py --model iML1515 --run 02_alphaKIV_id_mapping_and_pathway_validation
```

## Literature integration
Put the attached review at:
`data/raw/literature/attached_review.pdf`

The parser creates:
- `data/processed/literature_extracts/literature_claims.csv`
- `results/reports/literature_alignment.md`

## Notes
This scaffold intentionally distinguishes what is **directly modelable**, **proxy-modelable**, and **outside FBA scope**. Some heavy steps are left as structured stubs with logging hooks so the pipeline fails gracefully while remaining reproducible.
