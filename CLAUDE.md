# Project Context

This is an HPC research project. You are helping accelerate research the author already knows how to do. Your job is to write and debug code, not to design the research.

## Structure
- `methodology.md` — the research plan (five methodology questions). Read this first; it defines what every script should do.
- `data/raw/` — original data (not in Git)
- `data/processed/` — cleaned, analysis-ready data (not in Git)
- `scripts/` — `download_data.py`, `build_dataset.py`, `train_model.py`, `evaluate.py`
- `results/` — `metrics.json`, predictions, trained models (not in Git)
- `figures/` — publication-quality figures (300 DPI, labeled axes)
- `jobs/` — Slurm submission scripts for Vista

## Conventions
- Read `methodology.md` before writing any pipeline code.
- No spaces in filenames; lowercase; scripts named by what they do.
- Large data and trained models stay out of Git and live on Vista `$SCRATCH`.
- Heavy compute (training, SHAP) runs on Vista via `jobs/`, not on the laptop.
- Save figures to `figures/` at 300 DPI with labeled axes and a colorblind-friendly palette.

## How to help
- When asked to build the pipeline, follow `methodology.md` exactly.
- Verify any citations or factual claims; do not invent references.
- When a step needs HPC, write or edit a Slurm script in `jobs/` rather than running it locally.
