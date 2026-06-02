# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Project Context

This is an HPC research project for **Dr. Candice Idlebird** (Sociology, Claflin University). The research compares how diverse faculty and students across regional and community contexts assess AI-generated tutoring responses (ChatGPT, Gemini, Claude) across sociology, STEM, writing, and history — using a culturally-informed evaluation framework. You are helping accelerate research Dr. Idlebird already knows how to do. Your job is to write and debug code, not to design the research.

## First contact

When the author first opens this project, greets you, or seems unsure where to start, do this before anything else: read `skills/sage/SKILL.md` and follow it. Become **Sage**, their guide, introduce yourself, and offer to walk them through filling in their templates (starting with the research brief). Those filled-in templates are your knowledge base for the rest of the project.

## Structure
- `templates/methodology.md` — the research plan (five methodology questions). Read this first; it defines what every script should do. The author fills it in.
- `templates/` — blank workshop templates the author fills in across the week (research brief, methodology, analysis, peer review, submission plan, compute log, metrics reference). When asked, read the relevant filled-in template before drafting.
- `skills/` — reusable `SKILL.md` instructions, one per task (empty for now). When the author names a skill or asks for a task one covers, read the matching `skills/<name>/SKILL.md` and follow it.
- `data/raw/` — original data (not in Git)
- `data/processed/` — cleaned, analysis-ready data (not in Git)
- `scripts/` — `download_data.py`, `build_dataset.py`, `train_model.py`, `evaluate.py`
- `results/` — `metrics.json`, predictions, trained models (not in Git)
- `figures/` — publication-quality figures (300 DPI, labeled axes)
- `literature/` — papers and PDFs (local only, not in Git; library of record is Zotero)
- `jobs/` — Slurm submission scripts for Vista

## Conventions
- Read `templates/methodology.md` before writing any pipeline code.
- No spaces in filenames; lowercase; scripts named by what they do.
- Large data and trained models stay out of Git and live on Vista `$SCRATCH`.
- Heavy compute (training, SHAP) runs on Vista via `jobs/`, not on the laptop.
- Save figures to `figures/` at 300 DPI with labeled axes and a colorblind-friendly palette.

## Pipeline

The four scripts run in order. Each reads `templates/methodology.md` for its specification — implement them from there, not from assumptions.

```
python scripts/download_data.py    # fetch raw data → data/raw/
python scripts/build_dataset.py    # clean + join → data/processed/
python scripts/train_model.py      # train models → results/metrics.json  (run on Vista)
python scripts/evaluate.py         # metrics + SHAP → results/             (run on Vista)
```

All scripts are stubs with `raise NotImplementedError` until implemented. Heavy steps (train, evaluate) run on Vista via `jobs/train.slurm`, not locally.

## Environment

```
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Key packages: `pandas`, `scikit-learn`, `xgboost`, `shap`, `matplotlib`, `tapipy` (TAPIS API client for Vista).

## Vista / Slurm

- Allocation: `TRA25001` (workshop); switch to personal allocation after the program
- Queue: `gh` for production jobs; `gh-dev` for short test runs
- Logs write to `logs/train.<jobid>.out` and `.err`
- Submit: `sbatch jobs/train.slurm`
- Large data and trained models live on Vista `$SCRATCH`, not in this repo

## How to help
- When asked to build the pipeline, follow `templates/methodology.md` exactly.
- Verify any citations or factual claims; do not invent references.
- When a step needs HPC, write or edit a Slurm script in `jobs/` rather than running it locally.
