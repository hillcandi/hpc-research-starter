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
| `methodology.md` | Your five methodology questions. The AI reads this to write your scripts. |
| `data/raw/` | Original downloaded data. Not tracked in Git (lives on Vista `$SCRATCH`). |
| `data/processed/` | Cleaned, joined, analysis-ready data. Not tracked in Git. |
| `scripts/` | Your pipeline: download, build dataset, train, evaluate. |
| `notebooks/` | Interactive exploration. |
| `results/` | Metrics, predictions, trained models. Not tracked in Git. |
| `figures/` | Publication-quality figures (tracked; they go in the paper). |
| `jobs/` | Slurm/Tapis job submission scripts for Vista. |

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## The workflow

1. Fill in `methodology.md` (your five questions).
2. Ask your AI tool: *"Read methodology.md and implement scripts/build_dataset.py to produce the analysis table described there."*
3. Stage data on Vista, submit `jobs/train.slurm` to the `gh` queue via Tapis.
4. Read your metrics, generate figures, write the paper.

You bring the research. The scaffold, the AI tools, and HPC make it faster.
