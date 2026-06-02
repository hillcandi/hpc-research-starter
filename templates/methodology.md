# Methodology Document

**Name:** Dr. Candice Idlebird
**Date:** 2026-06-02
**Research Question:** How do diverse faculty and students across regional and community contexts differentially assess AI-generated tutoring responses, as measured by a culturally-informed evaluation framework applied within Google's Amplify platform?

This is your project's plan. Your AI tools read it to help you build, so be specific. It works for any kind of HPC computation, not only machine learning.

---

## 1. What Is Your Computation?

What kind of computation does your research need? Check the one that fits best (you can combine):

- [ ] **Machine learning / predictive model** — predict or classify an outcome from data
- [ ] **Simulation or numerical model** — model how a system behaves over time or under conditions
- [x] **Large-scale data processing / pipeline** — clean, join, or transform data too big for a laptop
- [x] **Statistical analysis** — test relationships or differences at scale (regression, Bayesian, bootstrapping)
- [ ] **Optimization / parameter sweep** — search many configurations for the best one
- [ ] **Other / domain-specific:** _______________

**In one sentence, what will your computation do?**

Run three generative AI tutoring models (ChatGPT, Gemini, and Claude) through a culturally-informed evaluation framework, then statistically compare how diverse faculty and student evaluators from different regional and community contexts rate each model's responses.



---

## 2. What Goes In?

**Unit of analysis:** Each row or record represents a single evaluator's rating of one AI-generated tutoring response (one evaluator × one model × one subject area × one prompt)

**Data sources:**

| Dataset | Source | Key Variables Used | Join Key |
|---------|--------|--------------------|----------|
| Participant evaluation ratings | Researcher-collected via culturally-informed framework | Evaluator role, region, institution type, model rated, subject area, framework scores | Evaluator ID |
| AI-generated tutoring responses | ChatGPT, Gemini, Claude — prompted across sociology, STEM, writing, and history | Model, subject area, prompt, response text | Prompt ID |
| IPEDS | nces.ed.gov/ipeds | Institution type (HBCU/MSI), enrollment by race/ethnicity, region | Institution ID |

**Approximate size:** ~TBD records x ~15 variables

**Data quality notes:** Sample size depends on participant recruitment; evaluator ratings are self-reported; AI responses may vary across model versions — model versions should be locked at time of data collection.



---

## 3. What Comes Out?

**What does your computation produce?** _(a prediction, a simulated dataset, a processed table, a statistical result, an optimal configuration, etc.)_

Comparative evaluation scores showing how ChatGPT, Gemini, and Claude are rated differently by faculty and students across regional and community contexts, broken down by subject area (sociology, STEM, writing, and history) and evaluator background.

**Form of the output:**
- [ ] A number (continuous)
- [ ] A category or label
- [ ] A time series
- [ ] Clusters or patterns
- [ ] A simulated or processed dataset
- [x] A statistical result (effect size, interval, posterior, etc.)
- [ ] Other: _______________

---

## 4. What Is Your Method?

**The approach you will use:** Comparative statistical analysis — ANOVA or mixed-effects regression to test whether evaluation scores differ significantly across evaluator demographics (role, region, institution type) and AI models (ChatGPT, Gemini, Claude), controlling for subject area.

**Why this approach over alternatives:** Mixed-effects regression accounts for the nested structure of the data (multiple ratings per evaluator) and handles variation across institutions and regions — better than simple ANOVA for this design.

**Your baseline or point of comparison:** _(the simpler result you compare against)_

Average evaluation scores with no demographic breakdown — the null assumption that all evaluators rate AI responses the same way regardless of cultural background.



### If your computation is machine learning

_Skip this block if you are not training a model._

**Standard features (from raw data):**

| Feature | Source Dataset | Type |
|---------|---------------|------|
| | | Continuous / Categorical |
| | | Continuous / Categorical |

**Engineered features (created from raw data):**

| Feature | How It's Computed | Why It Matters |
|---------|-------------------|----------------|
| | | |

**Which features are novel?** _(often the publishable contribution)_

**Baseline model:** ____________   **Primary model:** ____________

**Interpretability approach:** SHAP / built-in feature importance / partial dependence / other: ____________

---

## 5. How Do You Know It Worked?

Match your evaluation to your method:

- **Machine learning:** train/test split, metrics (RMSE, accuracy, F1, AUC), comparison to baseline
- **Simulation:** validation against known cases, convergence, sensitivity analysis
- **Data pipeline:** correctness and completeness checks, reproducibility
- **Statistics:** significance, effect size, model fit, assumptions checked
- **Optimization:** objective value, comparison to the baseline configuration

**Your evaluation plan:**

| What you check | Why |
|--------|-----------------|
| Statistically significant differences in evaluation scores across evaluator groups | Confirms cultural position shapes AI assessment |
| Effect sizes across models and subject areas | Shows which models and topics show the strongest cultural divergence |
| Model fit and assumptions (normality, independence) | Validates the statistical approach |
| Inter-rater reliability within demographic groups | Confirms the evaluation framework is being applied consistently |

**What does a "good" result look like for your question?**

Significant variation in how HBCU faculty and students versus other groups rate AI tutoring responses — especially differences across ChatGPT, Gemini, and Claude and across subject areas (sociology, STEM, writing, history).

**Would a negative or null result still be worth reporting?**

Yes — if all evaluators rate AI responses similarly regardless of cultural context, that is itself a finding that challenges or refines the gap argument and contributes to the field.



---

## Data Pipeline Diagram

_Draw or describe the flow from inputs to results. Show each source, how they combine, where the heavy compute happens, and what comes out._

```
[Tutoring prompts (4 subject areas)] ---\
                                         \
[ChatGPT, Gemini, Claude APIs] ----------> [Generate AI responses] --> [Evaluation instrument]
                                         /                                      |
[IPEDS + participant demographics] -----/                                       |
                                                                                v
                                                              [Evaluator ratings dataset]
                                                                                |
                                                                                v
                                                    [Mixed-effects regression / ANOVA on Vista]
                                                                                |
                                                                                v
                                                         [Comparative results + figures]
```

---

## Computational Plan

| Step | What Happens | Where | Queue | Estimated Time |
|------|-------------|-------|-------|----------------|
| Generate AI responses | Prompt ChatGPT, Gemini, Claude across 4 subject areas | Laptop / API | N/A | 1–2 hours |
| Participant data collection | Administer culturally-informed evaluation instrument to faculty and students | Survey platform | N/A | 1–2 weeks |
| Preprocessing | Clean and join evaluation ratings with IPEDS demographics | Laptop / Login node | N/A | 2–4 hours |
| Main computation | Run mixed-effects regression and ANOVA across all model/evaluator combinations | Vista | gh | 4–8 hours |
| Evaluation / analysis | Check model fit, effect sizes, inter-rater reliability | Vista / Laptop | N/A | 2–4 hours |
| Visualization | Generate comparison figures by model, subject area, and evaluator group | Laptop / Jupyter | N/A | 2–3 hours |

**Total estimated allocation usage:** ~12–16 node-hours

---

## Self-Check

Before moving to Compute, confirm:

- [ ] I have named what kind of computation this is
- [ ] My method is specific enough that someone else could run this study
- [ ] I have identified how my data sources connect
- [ ] I have a clear way to tell whether the result is good
- [ ] I know which steps need HPC and which do not
- [ ] My plan fits the time I have on Vista this week
