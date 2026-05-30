# HPC Research Starter

A starter scaffold for running your research on HPC with AI-assisted workflows. Clone it, drop your own research into the structure, and use AI coding tools (Claude Code, Cursor) plus Tapis/Slurm on Vista to accelerate work you already know how to do.

## How to use this during the workshop

1. **Make it yours.** On GitHub, click **Use this template** (or fork) to create a copy under your own account. Your work lives in your repo.
2. **Want help?** Add `ashleyscruse` as a collaborator on your copy (Settings → Collaborators). That lets me look at your code and help when you're stuck. Your work stays yours.
3. **Pull workshop additions.** If shared materials get added to the starter during the week, add it as a remote and pull from `main`:
   ```bash
   git remote add upstream <starter-repo-url>
   git pull upstream main
   ```

## Structure

| Path | What goes here |
|---|---|
| `CLAUDE.md` | Project context the AI reads. Keep it current so Claude Code knows your project. |
| `templates/` | Blank workshop templates: research brief, methodology, analysis, metrics reference, peer review, submission plan, compute log. Fill these in as you go; your AI prompts read them. `templates/methodology.md` is the one the pipeline scripts read. |
| `data/raw/` | Original downloaded data. Not tracked in Git (lives on Vista `$SCRATCH`). |
| `data/processed/` | Cleaned, joined, analysis-ready data. Not tracked in Git. |
| `scripts/` | Your pipeline: download, build dataset, train, evaluate. |
| `notebooks/` | Interactive exploration. |
| `results/` | Metrics, predictions, trained models. Not tracked in Git. |
| `figures/` | Publication-quality figures (tracked; they go in the paper). |
| `literature/` | Your papers and PDFs. Kept local, **not** in Git (copyrighted work shouldn't go to GitHub, and PDFs eat storage). Your library of record is Zotero; on a new machine just recreate an empty `literature/` folder. |
| `jobs/` | Slurm/Tapis job submission scripts for Vista. |

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## The workflow

The framework has five stages. The pattern is the same at every stage: **you make the decision in a template, point the AI at it, and review what it produces.** You bring the research; the scaffold, the AI tools, and HPC make it faster.

**Start here:** [**SETUP.md**](SETUP.md) shows how to get this repo onto your machine and open it in your tool (VS Code, Cursor, Antigravity, Claude Code, the Claude desktop app, or Claude on the web). Once it's open, say hi — you'll meet **Sage**, your guide, who walks you through filling in your first templates.

| Stage | You fill in | The AI helps | Output |
|---|---|---|---|
| 1 · Ideation | `templates/research-brief.md` | survey and verify the literature | question, gap, data, venue |
| 2 · Design | `templates/methodology.md` | — (you answer the five questions) | the plan every script reads |
| 3 · Compute | — | write the pipeline scripts, then run them on Vista | data on Vista, raw results |
| 4 · Analysis | `templates/analysis.md` | read metrics + SHAP, make figures | interpretation + figures |
| 5 · Publication | `templates/submission-plan.md` | assemble the paper | venue-formatted draft |

A typical loop:

1. Fill in the stage's template (start with `templates/methodology.md`).
2. Point the AI at it, e.g. *"Read templates/methodology.md and write scripts/build_dataset.py to produce the analysis table described there."*
3. Review what it produced. You decide; the AI accelerates.
4. Stage data on Vista and submit `jobs/train.slurm` to the `gh` queue, then interpret, visualize, and write.

## Skills

`skills/` is where reusable `SKILL.md` instructions live, so you can package a repeatable task once and use it in any tool (Claude Code, Cursor, VS Code, or Claude on the web). It currently includes **Sage**, your setup guide; see [`skills/README.md`](skills/README.md) for the list and how to add more.

---

## Credits

Created by **Ashley Scruse, Ph.D.** — [ashleyscruse.com](https://ashleyscruse.com). © 2026 Ashley Scruse. All rights reserved. See [NOTICE](NOTICE).
