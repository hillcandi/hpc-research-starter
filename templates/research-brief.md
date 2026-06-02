# Research Brief

**Name:** Candice Idlebird
**Date:** 2026-06-02
**Institution:** Claflin University
**Discipline:** Sociology

---

## 1. Research Question

_State your research question in one sentence._

How do diverse faculty and students across regional and community contexts differentially assess AI-generated tutoring responses, as measured by a culturally-informed evaluation framework applied within Google's Amplify platform?

**Why does this question need HPC?**

Large-scale model comparisons across multiple AI tutoring systems require compute beyond what a laptop can handle.

---

## 2. Gap It Fills

**What has been well-studied in this area?**

AI tutoring effectiveness, LLM evaluation methods, and cultural bias in NLP.

**What has NOT been done?**

Prior work has studied AI tutoring effectiveness and cultural bias in NLP separately, but no study has systematically examined how evaluators from diverse regional and community contexts — particularly students and faculty at minority-serving institutions — differentially assess AI-generated educational responses using a culturally-informed framework. The evaluator's cultural position has been largely absent from AI tutoring evaluation research.

**Why does this gap matter?**

As AI tutoring tools are deployed at scale in higher education, their effectiveness is increasingly evaluated without accounting for the cultural backgrounds of the students and faculty they serve. If evaluation frameworks remain culturally neutral on paper but biased in practice, institutions serving diverse and underrepresented communities — including HBCUs — risk adopting tools that systematically underserve their students. This research matters because equitable AI in education depends on who gets to define what "good" tutoring looks like.

**Key papers that define the current state (3-5):**

| # | Title | Authors | Year | Key Finding |
|---|-------|---------|------|-------------|
| 1 | Language (Technology) is Power: A Critical Survey of "Bias" in NLP | Blodgett et al. | 2020 | NLP bias research often lacks grounding in how bias harms real communities |
| 2 | Toward a Theory of Culturally Relevant Pedagogy | Ladson-Billings | 1995 | Effective teaching must affirm students' cultural identity — directly relevant to culturally-informed evaluation frameworks |
| 3 | On the Dangers of Stochastic Parrots: Can Language Models Be Too Big? | Bender et al. | 2021 | Large LMs encode cultural and social biases with real-world consequences |
| 4 | Algorithms of Oppression | Noble | 2018 | Search algorithms encode racial and cultural bias with real social consequences |
| 5 | Race After Technology | Benjamin | 2019 | Technological systems reproduce racial inequity through seemingly neutral design |
| 6 | Culturally Responsive Teaching: Theory, Research, and Practice | Gay | 2018 | Defines the pedagogical framework the evaluation instrument draws from |
| 7 | Culturally Sustaining Pedagogy: A Needed Change in Stance, Terminology, and Practice | Paris | 2012 | Extends culturally relevant pedagogy — useful for framing evaluation criteria |
| 8 | Systematic Review of Research on AI Applications in Higher Education | Zawacki-Richter et al. | 2019 | Maps the landscape of AI ed-tech — situates this research within the field |
| 9 | Stereotype Threat and the Intellectual Test Performance of African Americans | Steele & Aronson | 1995 | Foundational — supports why cultural context shapes how students experience AI feedback |
| 10 | The Impact of Generative AI Tools on Academic Performance in Higher Education: A Systematic Review | (ResearchGate) | 2023–2025 | Systematic review — useful for situating this study in current literature |
| 11 | AI Tutoring Outperforms In-Class Active Learning: An RCT | (Scientific Reports) | 2025 | RCT measuring AI tutor vs. active learning — strong comparison point |
| 12 | Custom Generative AI Tutors in Action: Experimental Evaluation of Prompt Strategies in STEM Education | (MDPI) | 2025 | Evaluates prompt strategies in AI tutoring — relevant to the evaluation framework |
| 13 | What the Research Shows About Generative AI in Tutoring | Brookings | 2026 | Flags concerns about accuracy, pedagogy, and dependence — supports the gap argument |
| 14 | Generative AI Ethical Considerations and Discriminatory Biases on Diverse Students Within the Classroom | (ResearchGate) | 2024 | Directly addresses how GenAI bias impacts diverse learners — core to the research argument |
| 15 | Do Tutors Learn from Equity Training and Can Generative AI Assess It? | (arXiv) | 2024 | Examines AI assessment of equity competencies — closely aligned with the evaluation framework |
| 16 | Promoting Equity and Addressing Concerns in Teaching and Learning with AI | Frontiers in Education | 2024 | Proposes actionable equity frameworks for AI in education |
| 17 | The Potential Impact of AI on Equity and Inclusion in Education | OECD | 2024 | Institutional-level report on AI equity — strong for situating HBCU context |

---

## 3. Data Sources

**Primary dataset:**

| Field | Details |
|-------|---------|
| Name | Participant Evaluation Ratings (collected by researcher) |
| Source URL | Collected via culturally-informed evaluation framework instrument |
| Format | Survey / rating data |
| Size | TBD based on participant recruitment |
| Key variables | Evaluator demographics (role, region, institution type), AI model evaluated, evaluation scores per framework dimension |
| Geographic scope | Regional and community contexts — HBCUs and minority-serving institutions |
| Temporal scope | Data collection period TBD |
| Access method | Researcher-collected |
| Known limitations | Sample size dependent on participant recruitment; self-reported evaluations |

**Supporting dataset(s):**

| Field | Dataset 2 | Dataset 3 |
|-------|-----------|-----------|
| Name | IPEDS (Integrated Postsecondary Education Data System) | Cross-National AI Attitudes Survey |
| Source URL | https://nces.ed.gov/ipeds | https://pmc.ncbi.nlm.nih.gov/articles/PMC12545832/ |
| Format | CSV / downloadable tables | Survey dataset (PMC open access) |
| Key variables | Institution type (HBCU/MSI), enrollment by race/ethnicity, region | Student attitudes toward AI, country/cultural context, demographics |
| Join key | Institution type / region | Cultural context / evaluator demographics |

**How do the datasets connect?**

IPEDS provides institutional demographic context to describe and validate the participant sample (HBCU and MSI enrollment by race/ethnicity and region). The Cross-National AI Attitudes Survey provides a comparison baseline for how students across different cultural contexts perceive AI, supporting the argument that cultural position shapes AI evaluation.



---

## 4. Target Venues

| # | Venue Name | Type | Next Deadline | Page Limit | Why It Fits |
|---|-----------|------|---------------|-----------|-------------|
| 1 | | Conference / Journal | | | |
| 2 | | Conference / Journal | | | |
| 3 | | Conference / Journal | | | |

---

## 5. Proposed Approach (brief)

**What method will you use?** (e.g., XGBoost, Random Forest, LSTM, etc.)

Comparative statistical analysis — ANOVA or mixed-effects regression to test whether evaluation scores differ significantly across evaluator demographics (role, region, institution type) and AI models (ChatGPT, Gemini, Claude), controlling for subject area (sociology, STEM, writing, history).

**What is your outcome variable?**

Evaluation scores from the culturally-informed framework — ratings assigned by diverse faculty and students to AI-generated tutoring responses.

**What are your key features?**

Evaluator role (faculty/student), evaluator region, institution type (HBCU/MSI), AI model evaluated, subject area of tutoring prompt.

**What does success look like?** (What result would be worth publishing?)

Statistically significant differences in how evaluators from different cultural and regional contexts rate AI tutoring responses — demonstrating that the evaluator's cultural position meaningfully shapes AI assessment outcomes.



---

## Self-Check

Before moving to Stage 2 (Design), confirm:

- [ ] My question is specific enough that someone else would know exactly what I'm studying
- [ ] The gap is real (not already addressed in published work)
- [ ] I have at least one dataset I can access this week
- [ ] I have identified at least one venue where this work fits
- [ ] This question benefits from HPC (not solvable on a laptop)
