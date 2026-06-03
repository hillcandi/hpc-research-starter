"""Statistical analysis: mixed-effects regression and ANOVA across evaluator groups.

Reads:  data/processed/analysis_dataset.csv
Writes: results/metrics.json        — all statistical results
        results/model_summaries/    — full regression output per score dimension

Run on Vista via jobs/train.slurm, not locally.

Method per methodology.md Section 4:
  - Mixed-effects linear regression: tests whether evaluation scores differ
    significantly across evaluator demographics (role, region, institution_type)
    and AI models, controlling for subject area.
  - One-way ANOVA: tests main effects of model and institution_type per score.
  - Baseline: grand mean scores per model with no demographic breakdown.
"""

import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

warnings.filterwarnings("ignore")

PROCESSED = Path("data/processed")
RESULTS = Path("results")
RESULTS.mkdir(parents=True, exist_ok=True)
SUMMARIES = RESULTS / "model_summaries"
SUMMARIES.mkdir(parents=True, exist_ok=True)

SCORE_COLS = [
    "score_accuracy",
    "score_clarity",
    "score_cultural_relevance",
    "score_engagement",
    "score_overall",
]

MODELS = ["ChatGPT", "Gemini", "Claude"]
SUBJECT_AREAS = ["sociology", "STEM", "writing", "history"]


def load_data():
    path = PROCESSED / "analysis_dataset.csv"
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Run build_dataset.py first."
        )
    df = pd.read_csv(path)
    print(f"  Loaded {len(df)} rows, {len(df.columns)} columns")
    return df


def baseline_analysis(df):
    """Grand mean scores per model — null assumption of no group differences."""
    print("  Computing baseline (grand means per model)...")
    baseline = (
        df.groupby("model")[SCORE_COLS + ["score_framework_mean"]]
        .agg(["mean", "std", "count"])
        .round(4)
    )
    return baseline.to_dict()


def run_anova(df, grouping_var, score_col):
    """One-way ANOVA: does score differ significantly across groups?"""
    groups = [
        grp[score_col].dropna().values
        for _, grp in df.groupby(grouping_var)
        if len(grp[score_col].dropna()) >= 2
    ]
    if len(groups) < 2:
        return {"f_stat": None, "p_value": None, "note": "insufficient groups"}
    f_stat, p_value = stats.f_oneway(*groups)
    return {
        "f_stat": round(float(f_stat), 4),
        "p_value": round(float(p_value), 4),
        "significant_p05": bool(p_value < 0.05),
    }


def compute_effect_size_eta2(df, grouping_var, score_col):
    """Eta-squared effect size for ANOVA (proportion of variance explained)."""
    grand_mean = df[score_col].mean()
    groups = df.groupby(grouping_var)[score_col]
    ss_between = sum(
        len(g) * (g.mean() - grand_mean) ** 2
        for _, g in groups
    )
    ss_total = ((df[score_col] - grand_mean) ** 2).sum()
    if ss_total == 0:
        return None
    return round(float(ss_between / ss_total), 4)


def run_mixed_effects(df, score_col):
    """
    Mixed-effects linear regression for one score dimension.
    Fixed effects: model, institution_type, evaluator_role, subject_area, region
    Random effect: evaluator_id (accounts for multiple ratings per person)
    Falls back to OLS if statsmodels MixedLM fails (e.g. insufficient data).
    """
    try:
        import statsmodels.formula.api as smf
    except ImportError:
        return {"error": "statsmodels not installed — run pip install statsmodels"}

    # Encode categorical predictors
    sub = df[[score_col, "model", "institution_type", "evaluator_role",
              "subject_area", "region", "evaluator_id"]].dropna()

    if len(sub) < 20:
        return {"error": f"Insufficient data for mixed model ({len(sub)} rows)"}

    formula = (
        f"{score_col} ~ C(model) + C(institution_type) + "
        f"C(evaluator_role) + C(subject_area) + C(region)"
    )

    try:
        model = smf.mixedlm(formula, sub, groups=sub["evaluator_id"])
        result = model.fit(reml=True)

        # Save full summary to file
        summary_path = SUMMARIES / f"mixedlm_{score_col}.txt"
        with open(summary_path, "w") as f:
            f.write(result.summary().as_text())

        # Extract key fixed-effect coefficients
        coefs = {}
        for name, coef, pval in zip(
            result.params.index,
            result.params.values,
            result.pvalues.values,
        ):
            coefs[name] = {
                "coef": round(float(coef), 4),
                "p_value": round(float(pval), 4),
                "significant_p05": bool(pval < 0.05),
            }
        return {
            "method": "mixed_effects_lm",
            "n_obs": int(len(sub)),
            "log_likelihood": round(float(result.llf), 4),
            "coefficients": coefs,
        }

    except Exception as e:
        # Fallback: OLS regression (ignores nesting but still useful)
        try:
            ols = smf.ols(formula, sub).fit()
            return {
                "method": "ols_fallback",
                "note": str(e),
                "n_obs": int(len(sub)),
                "r_squared": round(float(ols.rsquared), 4),
                "f_stat": round(float(ols.fvalue), 4),
                "f_pvalue": round(float(ols.f_pvalue), 4),
            }
        except Exception as e2:
            return {"error": str(e2)}


def inter_rater_reliability(df):
    """
    Krippendorff's alpha approximation via pairwise ICC per model+subject group.
    Reports mean pairwise correlation across evaluator pairs as a proxy.
    """
    results = {}
    for model in MODELS:
        for subject in SUBJECT_AREAS:
            grp = df[(df["model"] == model) & (df["subject_area"] == subject)]
            if len(grp) < 3:
                continue
            scores = grp[SCORE_COLS].dropna()
            if len(scores) < 3:
                continue
            # Mean inter-item correlation across score dimensions
            corr_matrix = scores.corr()
            upper = corr_matrix.where(
                np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
            )
            mean_corr = upper.stack().mean()
            results[f"{model}_{subject}"] = round(float(mean_corr), 4)
    return results


def main():
    print("=== train_model.py (statistical analysis) ===\n")

    print("1. Loading processed data...")
    df = load_data()

    metrics = {}

    print("\n2. Baseline analysis (grand means per model)...")
    metrics["baseline"] = baseline_analysis(df)

    print("\n3. ANOVA: effect of model and institution type on each score...")
    anova_results = {}
    for score in SCORE_COLS:
        anova_results[score] = {
            "by_model": run_anova(df, "model", score),
            "by_institution_type": run_anova(df, "institution_type", score),
            "by_evaluator_role": run_anova(df, "evaluator_role", score),
            "by_subject_area": run_anova(df, "subject_area", score),
            "eta2_model": compute_effect_size_eta2(df, "model", score),
            "eta2_institution_type": compute_effect_size_eta2(df, "institution_type", score),
        }
    metrics["anova"] = anova_results

    print("\n4. Mixed-effects regression per score dimension...")
    mixed_results = {}
    for score in SCORE_COLS:
        print(f"  Running: {score}")
        mixed_results[score] = run_mixed_effects(df, score)
    metrics["mixed_effects"] = mixed_results

    print("\n5. Inter-rater reliability...")
    metrics["inter_rater_reliability"] = inter_rater_reliability(df)

    print("\n6. Saving results...")
    out = RESULTS / "metrics.json"
    with open(out, "w") as f:
        json.dump(metrics, f, indent=2, default=str)
    print(f"  metrics.json → {out}")
    print(f"  Full model summaries → {SUMMARIES}/")

    # Print headline findings
    print("\n=== Headline Results ===")
    for score in SCORE_COLS:
        anova = metrics["anova"][score]["by_model"]
        sig = anova.get("significant_p05", False)
        p = anova.get("p_value", "N/A")
        eta2 = metrics["anova"][score].get("eta2_model", "N/A")
        print(f"  {score}: model effect p={p}, η²={eta2}, significant={sig}")

    print("\nDone. Run evaluate.py next for figures and full interpretation.")


if __name__ == "__main__":
    main()
