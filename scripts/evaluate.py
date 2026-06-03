"""Evaluate statistical results and generate publication-quality figures.

Reads:  data/processed/analysis_dataset.csv
        results/metrics.json
Writes: figures/                    — all plots at 300 DPI
        results/interpretation.txt  — plain-language summary of findings

Run on Vista after train_model.py completes.
Figures per methodology.md: compare models × subject areas × evaluator groups.
"""

import json
import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd

PROCESSED = Path("data/processed")
RESULTS = Path("results")
FIGURES = Path("figures")
FIGURES.mkdir(parents=True, exist_ok=True)

SCORE_COLS = [
    "score_accuracy",
    "score_clarity",
    "score_cultural_relevance",
    "score_engagement",
    "score_overall",
]

SCORE_LABELS = {
    "score_accuracy": "Accuracy",
    "score_clarity": "Clarity",
    "score_cultural_relevance": "Cultural Relevance",
    "score_engagement": "Engagement",
    "score_overall": "Overall",
    "score_framework_mean": "Framework Mean",
}

MODELS = ["ChatGPT", "Gemini", "Claude"]
SUBJECT_AREAS = ["sociology", "STEM", "writing", "history"]

# Colorblind-friendly palette (Wong 2011)
COLORS = {
    "ChatGPT": "#0072B2",   # blue
    "Gemini":  "#E69F00",   # orange
    "Claude":  "#009E73",   # green
    "HBCU":    "#D55E00",   # vermillion
    "MSI":     "#56B4E9",   # sky blue
    "OTHER":   "#999999",   # grey
    "faculty": "#CC79A7",   # pink
    "student": "#F0E442",   # yellow
}

FIGSIZE = (10, 6)
DPI = 300


def load_data():
    df = pd.read_csv(PROCESSED / "analysis_dataset.csv")
    with open(RESULTS / "metrics.json") as f:
        metrics = json.load(f)
    print(f"  Loaded {len(df)} rows for plotting")
    return df, metrics


def fig1_model_comparison(df):
    """Bar chart: mean scores across all 5 dimensions by model."""
    means = df.groupby("model")[SCORE_COLS].mean().reindex(MODELS)

    x = np.arange(len(SCORE_COLS))
    width = 0.25
    fig, ax = plt.subplots(figsize=FIGSIZE)

    for i, model in enumerate(MODELS):
        vals = [means.loc[model, s] if model in means.index else 0 for s in SCORE_COLS]
        ax.bar(x + i * width, vals, width, label=model,
               color=COLORS[model], edgecolor="white", linewidth=0.5)

    ax.set_xlabel("Evaluation Dimension", fontsize=12)
    ax.set_ylabel("Mean Score (1–5)", fontsize=12)
    ax.set_title("Mean Evaluation Scores by AI Model", fontsize=14, fontweight="bold")
    ax.set_xticks(x + width)
    ax.set_xticklabels([SCORE_LABELS[s] for s in SCORE_COLS], rotation=15, ha="right")
    ax.set_ylim(0, 5.5)
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.5))
    ax.legend(title="Model", framealpha=0.9)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    out = FIGURES / "fig1_model_comparison.png"
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    print(f"  Saved {out.name}")


def fig2_cultural_relevance_by_institution(df):
    """Bar chart: cultural relevance score by model × institution type (key finding)."""
    inst_types = ["HBCU", "MSI", "OTHER"]
    df["institution_type_upper"] = df["institution_type"].str.upper()
    means = (
        df.groupby(["model", "institution_type_upper"])["score_cultural_relevance"]
        .mean()
        .unstack("institution_type_upper")
        .reindex(MODELS)
        .reindex(columns=inst_types)
    )

    x = np.arange(len(MODELS))
    width = 0.25
    fig, ax = plt.subplots(figsize=FIGSIZE)

    for i, inst in enumerate(inst_types):
        vals = means[inst].fillna(0).values if inst in means.columns else np.zeros(len(MODELS))
        ax.bar(x + i * width, vals, width, label=inst,
               color=COLORS.get(inst, "#aaaaaa"), edgecolor="white", linewidth=0.5)

    ax.set_xlabel("AI Model", fontsize=12)
    ax.set_ylabel("Mean Cultural Relevance Score (1–5)", fontsize=12)
    ax.set_title(
        "Cultural Relevance Scores by AI Model and Institution Type",
        fontsize=14, fontweight="bold"
    )
    ax.set_xticks(x + width)
    ax.set_xticklabels(MODELS)
    ax.set_ylim(0, 5.5)
    ax.legend(title="Institution Type", framealpha=0.9)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    out = FIGURES / "fig2_cultural_relevance_by_institution.png"
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    print(f"  Saved {out.name}")


def fig3_heatmap_model_by_subject(df):
    """Heatmap: framework mean score by model × subject area."""
    pivot = (
        df.groupby(["model", "subject_area"])["score_framework_mean"]
        .mean()
        .unstack("subject_area")
        .reindex(MODELS)
        .reindex(columns=SUBJECT_AREAS)
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    im = ax.imshow(pivot.values, cmap="RdYlGn", vmin=1, vmax=5, aspect="auto")

    ax.set_xticks(range(len(SUBJECT_AREAS)))
    ax.set_xticklabels([s.title() for s in SUBJECT_AREAS], fontsize=11)
    ax.set_yticks(range(len(MODELS)))
    ax.set_yticklabels(MODELS, fontsize=11)
    ax.set_title(
        "Framework Mean Score by Model and Subject Area",
        fontsize=14, fontweight="bold", pad=12
    )

    # Annotate cells
    for i in range(len(MODELS)):
        for j in range(len(SUBJECT_AREAS)):
            val = pivot.values[i, j]
            if not np.isnan(val):
                ax.text(j, i, f"{val:.2f}", ha="center", va="center",
                        fontsize=10, color="black", fontweight="bold")

    cbar = fig.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label("Mean Score (1–5)", fontsize=10)
    fig.tight_layout()
    out = FIGURES / "fig3_heatmap_model_by_subject.png"
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    print(f"  Saved {out.name}")


def fig4_scores_by_evaluator_role(df):
    """Bar chart: framework mean score by model × evaluator role (faculty vs student)."""
    roles = df["evaluator_role"].dropna().unique().tolist()
    means = (
        df.groupby(["model", "evaluator_role"])["score_framework_mean"]
        .mean()
        .unstack("evaluator_role")
        .reindex(MODELS)
    )

    x = np.arange(len(MODELS))
    width = 0.35
    fig, ax = plt.subplots(figsize=FIGSIZE)

    for i, role in enumerate(roles):
        if role not in means.columns:
            continue
        ax.bar(x + i * width, means[role].fillna(0), width, label=role.title(),
               color=COLORS.get(role, "#aaaaaa"), edgecolor="white", linewidth=0.5)

    ax.set_xlabel("AI Model", fontsize=12)
    ax.set_ylabel("Mean Framework Score (1–5)", fontsize=12)
    ax.set_title(
        "Evaluation Scores by AI Model and Evaluator Role",
        fontsize=14, fontweight="bold"
    )
    ax.set_xticks(x + width / 2)
    ax.set_xticklabels(MODELS)
    ax.set_ylim(0, 5.5)
    ax.legend(title="Evaluator Role", framealpha=0.9)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    out = FIGURES / "fig4_scores_by_evaluator_role.png"
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    print(f"  Saved {out.name}")


def fig5_effect_sizes(metrics):
    """Bar chart: eta-squared effect sizes by score dimension."""
    scores = SCORE_COLS
    eta2_model = [
        metrics["anova"].get(s, {}).get("eta2_model") or 0 for s in scores
    ]
    eta2_inst = [
        metrics["anova"].get(s, {}).get("eta2_institution_type") or 0 for s in scores
    ]

    x = np.arange(len(scores))
    width = 0.35
    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.bar(x - width / 2, eta2_model, width, label="AI Model", color=COLORS["ChatGPT"])
    ax.bar(x + width / 2, eta2_inst, width, label="Institution Type", color=COLORS["HBCU"])

    ax.axhline(0.01, color="gray", linestyle="--", linewidth=0.8, label="Small effect (η²=0.01)")
    ax.axhline(0.06, color="gray", linestyle="-.", linewidth=0.8, label="Medium effect (η²=0.06)")

    ax.set_xlabel("Evaluation Dimension", fontsize=12)
    ax.set_ylabel("Eta-Squared (η²)", fontsize=12)
    ax.set_title("Effect Sizes: AI Model and Institution Type on Evaluation Scores",
                 fontsize=14, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels([SCORE_LABELS[s] for s in scores], rotation=15, ha="right")
    ax.legend(framealpha=0.9, fontsize=9)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    out = FIGURES / "fig5_effect_sizes.png"
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    print(f"  Saved {out.name}")


def write_interpretation(df, metrics):
    """Write plain-language summary of findings to results/interpretation.txt."""
    lines = [
        "=" * 60,
        "INTERPRETATION OF RESULTS",
        "Dr. Candice Idlebird — Claflin University — Sociology",
        "=" * 60,
        "",
        "Research Question:",
        textwrap.fill(
            "How do diverse faculty and students across regional and community "
            "contexts differentially assess AI-generated tutoring responses, as "
            "measured by a culturally-informed evaluation framework?",
            width=60
        ),
        "",
        "--- ANOVA Results (effect of AI model on each score) ---",
    ]

    for score in SCORE_COLS:
        anova = metrics["anova"].get(score, {}).get("by_model", {})
        eta2 = metrics["anova"].get(score, {}).get("eta2_model")
        p = anova.get("p_value", "N/A")
        sig = anova.get("significant_p05", False)
        lines.append(
            f"  {SCORE_LABELS[score]}: p={p}, η²={eta2}, "
            f"{'SIGNIFICANT' if sig else 'not significant'}"
        )

    lines += [
        "",
        "--- ANOVA Results (effect of institution type on each score) ---",
    ]
    for score in SCORE_COLS:
        anova = metrics["anova"].get(score, {}).get("by_institution_type", {})
        eta2 = metrics["anova"].get(score, {}).get("eta2_institution_type")
        p = anova.get("p_value", "N/A")
        sig = anova.get("significant_p05", False)
        lines.append(
            f"  {SCORE_LABELS[score]}: p={p}, η²={eta2}, "
            f"{'SIGNIFICANT' if sig else 'not significant'}"
        )

    lines += [
        "",
        "--- Figures Generated ---",
        "  fig1_model_comparison.png         — overall scores by model",
        "  fig2_cultural_relevance_by_institution.png — key finding",
        "  fig3_heatmap_model_by_subject.png — model × subject area",
        "  fig4_scores_by_evaluator_role.png — faculty vs student",
        "  fig5_effect_sizes.png             — eta-squared by dimension",
        "",
    ]

    out = RESULTS / "interpretation.txt"
    with open(out, "w") as f:
        f.write("\n".join(lines))
    print(f"  interpretation.txt → {out}")


def main():
    print("=== evaluate.py ===\n")

    print("1. Loading data and results...")
    df, metrics = load_data()

    print("\n2. Generating figures...")
    fig1_model_comparison(df)
    fig2_cultural_relevance_by_institution(df)
    fig3_heatmap_model_by_subject(df)
    fig4_scores_by_evaluator_role(df)
    fig5_effect_sizes(metrics)

    print("\n3. Writing interpretation...")
    write_interpretation(df, metrics)

    print(f"\nDone. All figures saved to {FIGURES}/ at 300 DPI.")
    print("Review figures/ and results/interpretation.txt for your findings.")


if __name__ == "__main__":
    main()
