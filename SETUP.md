# Setup — get the repo and meet Sage

Three steps: make your own copy, get it onto your computer, open it in your tool and say hi to Sage. **However you do it, the whole folder ends up on your machine.**

---

## Step 1 — Make your own copy

This keeps your work in your own account.

1. On this repo's GitHub page, click **Use this template → Create a new repository** (or **Fork** if you don't see that button).
2. Optional, if you want help during the workshop: your repo → **Settings → Collaborators → add `ashleyscruse`**. Your work stays yours; this just lets me look when you're stuck.

## Step 2 — Get it onto your computer

Pick whichever you're comfortable with. All give you the full folder:

- **Download ZIP (no git needed):** green **Code** button → **Download ZIP** → unzip it.
- **Git command line:** `git clone https://github.com/<your-username>/hpc-research-starter.git`
- **GitHub Desktop:** **Code → Open with GitHub Desktop → Clone.**

## Step 3 — Open it in your tool and meet Sage

The **universal move** in any tool: open the folder, then tell the AI:

> "Read CLAUDE.md and skills/sage/SKILL.md, then be Sage and guide me."

How each entry point works:

| Tool | How to open the folder | How to start Sage |
|---|---|---|
| **Claude Code** (the CLI "coworker") | `cd` into the folder, run `claude` | Just say **hi** — it reads `CLAUDE.md` automatically and Sage introduces herself |
| **Cursor** | File → Open Folder → your repo | Open chat (Cmd/Ctrl + L), paste the universal line |
| **VS Code + Copilot** | File → Open Folder → your repo | Open Copilot Chat, paste the universal line |
| **Antigravity** | Open the project folder | In the agent panel, paste the universal line |
| **Claude desktop app** | Create/open a Project, add this folder | Paste the universal line |
| **Claude on the web** (claude.ai) | No folder to mount here — **upload** `CLAUDE.md`, `skills/sage/SKILL.md`, and the template you're filling (start with `templates/research-brief.md`) into a Project or chat | Paste the universal line |

> **Claude Code** is the only one that reads `CLAUDE.md` on its own, so "hi" is enough. Everywhere else, the universal line points the AI at Sage. For **Claude on the web**, keep the downloaded folder on your computer so you can upload files in and save your work back out.

## What happens next

Sage gets your workspace set up and walks you through your **research brief** first, then your **methodology**. Those filled-in templates become the AI's knowledge base for the rest of the week — code, analysis, and writing all read from them.
