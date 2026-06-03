"""Clean and join raw data into an analysis-ready table in data/processed/.

Inputs (data/raw/):
  - ai_responses.csv          — ChatGPT, Gemini, Claude responses across 4 subject areas
  - evaluation_ratings.csv    — participant ratings using the culturally-informed framework
  - ipeds_hbcu.csv            — HBCU institution directory from IPEDS

Output (data/processed/):
  - analysis_dataset.csv      — one row per evaluator × model × subject area × prompt
  - summary_stats.csv         — mean scores by model, subject area, and evaluator group

Run after:
  python scripts/download_data.py  (and filling in ai_responses.csv and evaluation_ratings.csv)
"""

from pathlib import Path

import pandas as pd

RAW = Path("data/raw")
PROCESSED = Path("data/processed")
PROCESSED.mkdir(parents=True, exist_ok=True)

SCORE_COLS = [
    "score_accuracy",
    "score_clarity",
    "score_cultural_relevance",
    "score_engagement",
    "score_overall",
]


def load_and_validate(path, required_cols, label):
    if not path.exists():
        raise FileNotFoundError(
            f"{label} not found at {path}. "
            "See download_data.py instructions."
        )
    df = pd.read_csv(path)
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"{label} is missing columns: {missing}")
    print(f"  Loaded {len(df)} rows from {path.name}")
    return df


def clean_ratings(df):
    """Standardize and validate participant evaluation ratings."""
    df = df.copy()

    # Normalize text fields
    df["evaluator_role"] = df["evaluator_role"].str.strip().str.lower()
    df["institution_type"] = df["institution_type"].str.strip().str.upper()
    df["region"] = df["region"].str.strip().str.title()
    df["model"] = df["model"].str.strip()
    df["subject_area"] = df["subject_area"].str.strip().str.lower()

    # Drop rows missing any score
    before = len(df)
    df = df.dropna(subset=SCORE_COLS)
    dropped = before - len(df)
    if dropped:
        print(f"  Dropped {dropped} rows with missing scores")

    # Validate score range 1-5
    for col in SCORE_COLS:
        out_of_range = ~df[col].between(1, 5)
        if out_of_range.any():
            print(f"  WARNING: {out_of_range.sum()} values out of range in {col}")

    return df


def clean_ai_responses(df):
    """Standardize AI response data and assign prompt IDs."""
    df = df.copy()
    df["model"] = df["model"].str.strip()
    df["subject_area"] = df["subject_area"].str.strip().str.lower()

    # Assign a stable prompt_id from subject_area
    prompt_map = {s: i + 1 for i, s in enumerate(sorted(df["subject_area"].unique()))}
    df["prompt_id"] = df["subject_area"].map(prompt_map)

    # Drop rows with empty responses
    before = len(df)
    df = df[df["response"].notna() & (df["response"].str.strip() != "")]
    dropped = before - len(df)
    if dropped:
        print(f"  Dropped {dropped} AI response rows with empty text")

    return df


def enrich_with_ipeds(ratings, ipeds):
    """Join evaluator institution data with IPEDS for institution-level context."""
    ipeds_slim = ipeds[["unitid", "inst_name", "obereg", "locale"]].copy()
    ipeds_slim.columns = ["unitid", "ipeds_inst_name", "ipeds_region_code", "ipeds_locale"]

    merged = ratings.merge(
        ipeds_slim,
        left_on="institution_name",
        right_on="ipeds_inst_name",
        how="left",
    )
    unmatched = merged["unitid"].isna().sum()
    if unmatched:
        print(f"  {unmatched} evaluator rows did not match an IPEDS institution — check institution_name spelling")
    return merged


def engineer_features(df):
    """Add computed columns used in the analysis."""
    # Mean score across all framework dimensions (excluding overall)
    framework_cols = [c for c in SCORE_COLS if c != "score_overall"]
    df["score_framework_mean"] = df[framework_cols].mean(axis=1)

    # Binary flag: evaluator is at an HBCU
    df["is_hbcu"] = df["institution_type"].str.upper() == "HBCU"

    # Composite evaluator group label for analysis
    df["evaluator_group"] = df["institution_type"] + " / " + df["evaluator_role"].str.title()

    return df


def main():
    print("=== build_dataset.py ===\n")

    print("1. Loading raw data...")
    ratings = load_and_validate(
        RAW / "evaluation_ratings.csv",
        required_cols=["evaluator_id", "evaluator_role", "institution_name",
                       "institution_type", "region", "subject_area", "model"] + SCORE_COLS,
        label="Evaluation ratings",
    )
    ai_responses = load_and_validate(
        RAW / "ai_responses.csv",
        required_cols=["model", "subject_area", "prompt", "response"],
        label="AI responses",
    )
    ipeds = load_and_validate(
        RAW / "ipeds_hbcu.csv",
        required_cols=["unitid", "inst_name"],
        label="IPEDS HBCU",
    )

    print("\n2. Cleaning data...")
    ratings = clean_ratings(ratings)
    ai_responses = clean_ai_responses(ai_responses)

    print("\n3. Joining datasets...")
    # Attach AI response text to ratings on model + subject_area
    dataset = ratings.merge(
        ai_responses[["model", "subject_area", "prompt_id", "prompt", "response"]],
        on=["model", "subject_area"],
        how="left",
    )
    dataset = enrich_with_ipeds(dataset, ipeds)

    print("\n4. Engineering features...")
    dataset = engineer_features(dataset)

    print("\n5. Saving outputs...")
    out_main = PROCESSED / "analysis_dataset.csv"
    dataset.to_csv(out_main, index=False)
    print(f"  Analysis dataset → {out_main} ({len(dataset)} rows, {len(dataset.columns)} columns)")

    # Summary stats: mean scores by model × subject area × evaluator group
    summary = (
        dataset.groupby(["model", "subject_area", "evaluator_group"])[SCORE_COLS + ["score_framework_mean"]]
        .agg(["mean", "std", "count"])
        .round(3)
    )
    out_summary = PROCESSED / "summary_stats.csv"
    summary.to_csv(out_summary)
    print(f"  Summary stats     → {out_summary}")

    print("\nDone. Next step: run train_model.py on Vista.")
    print("  sbatch jobs/train.slurm")


if __name__ == "__main__":
    main()
