"""Download raw data into data/raw/.

Three sources per methodology.md Section 2:
  1. AI response template — prompts pre-filled; paste responses manually from the web
  2. IPEDS HBCU/MSI directory — via Urban Institute Education Data API (free, no auth)
  3. Evaluation instrument template — blank CSV for participant ratings

To collect AI responses:
  1. Run this script once to generate data/raw/ai_responses_template.csv
  2. Open that file and paste responses from chat.openai.com, gemini.google.com, claude.ai
  3. Save the file as data/raw/ai_responses.csv (keep the same columns)
  4. Run build_dataset.py
"""

import csv
import os
from pathlib import Path

import pandas as pd
import requests

RAW = Path("data/raw")
RAW.mkdir(parents=True, exist_ok=True)

PROMPTS = {
    "sociology": (
        "I'm a student learning about social stratification. "
        "Can you explain what it is and how it affects educational outcomes?"
    ),
    "STEM": (
        "I'm struggling with the Pythagorean theorem. "
        "Can you explain how it works and give me a real-world example?"
    ),
    "writing": (
        "Can you explain the difference between a thesis statement and a topic sentence? "
        "Please give examples of each."
    ),
    "history": (
        "Can you explain the main causes and significance of the Civil Rights Movement "
        "in the United States?"
    ),
}

MODELS = ["ChatGPT", "Gemini", "Claude"]


def write_ai_response_template():
    """Write a template CSV with prompts pre-filled and response column blank."""
    out = RAW / "ai_responses_template.csv"
    rows = []
    for model in MODELS:
        for subject, prompt in PROMPTS.items():
            rows.append({
                "model": model,
                "subject_area": subject,
                "prompt": prompt,
                "response": "",  # paste response here from the web interface
            })
    df = pd.DataFrame(rows)
    df.to_csv(out, index=False)
    print(f"  Template written → {out}")
    print(f"  Fill in the 'response' column for all {len(rows)} rows, then save as ai_responses.csv")


def check_ai_responses():
    """Check whether ai_responses.csv exists and is complete."""
    path = RAW / "ai_responses.csv"
    if not path.exists():
        print("  ai_responses.csv not found — fill in the template first.")
        return
    df = pd.read_csv(path)
    missing = df["response"].isna() | (df["response"].str.strip() == "")
    if missing.any():
        print(f"  WARNING: {missing.sum()} rows still have empty responses in ai_responses.csv")
    else:
        print(f"  ai_responses.csv looks complete ({len(df)} rows)")


def download_ipeds_hbcu():
    """Download HBCU institution directory via Urban Institute Education Data API."""
    print("  Fetching IPEDS HBCU directory...")
    url = "https://educationdata.urban.org/api/v1/schools/ipeds/directory/"
    params = {"hbcu": 1, "page_size": 500}

    all_records = []
    while url:
        resp = requests.get(url, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        all_records.extend(data.get("results", []))
        url = data.get("next")
        params = {}

    df = pd.DataFrame(all_records)
    out = RAW / "ipeds_hbcu.csv"
    df.to_csv(out, index=False)
    print(f"  Saved {len(df)} institutions → {out}")


def write_evaluation_template():
    """Write blank evaluation instrument CSV for participant data collection."""
    out = RAW / "evaluation_ratings_template.csv"
    fields = [
        "evaluator_id",
        "evaluator_role",            # faculty | student
        "institution_name",
        "institution_type",          # HBCU | MSI | other
        "region",
        "subject_area",              # sociology | STEM | writing | history
        "model",                     # ChatGPT | Gemini | Claude
        "prompt_id",
        "score_accuracy",            # 1-5
        "score_clarity",             # 1-5
        "score_cultural_relevance",  # 1-5
        "score_engagement",          # 1-5
        "score_overall",             # 1-5
        "comments",
    ]
    with open(out, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
    print(f"  Evaluation template → {out}")


def main():
    print("=== download_data.py ===\n")

    print("1. Writing AI response template (fill in manually from the web)...")
    write_ai_response_template()
    check_ai_responses()

    print("\n2. Downloading IPEDS HBCU data...")
    download_ipeds_hbcu()

    print("\n3. Writing evaluation instrument template...")
    write_evaluation_template()

    print("\nDone. data/raw/ contents:")
    for f in sorted(RAW.iterdir()):
        if f.name != ".gitkeep":
            print(f"  {f.name}")

    print("\nNext step:")
    print("  Open data/raw/ai_responses_template.csv")
    print("  Paste responses from chat.openai.com, gemini.google.com, and claude.ai")
    print("  Save as data/raw/ai_responses.csv")
    print("  Then run: python scripts/build_dataset.py")


if __name__ == "__main__":
    main()
