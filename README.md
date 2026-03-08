# MORPHD Personal Intelligence

> *An AI companion that knows you because you gave it your data.*

Built for the **Data Portability Hackathon 2026** — Track 2: AI Companions with Purpose
Organized by AITX, AI Collective Austin, Data Transfer Initiative, and UT School of Law

---

## What Is MORPHD Personal Intelligence?

MORPHD Personal Intelligence is an AI-powered companion that ingests a person's own longitudinal data — journals, biometrics, calendar, transactions, and conversation history — and surfaces the behavioral patterns and decision intelligence that are impossible to see from inside the day-to-day.

Most AI tools know you based on what you type in the moment. MORPHD knows you based on what you've *lived.*

---

## The Problem

Executives, founders, and high-performers are drowning in personal data they've never been able to use. Their sleep data lives in Whoop. Their thinking lives in journals. Their decisions live in emails and calendars. Their spending patterns live in bank exports.

None of it talks to each other. None of it tells them anything they couldn't already see themselves.

MORPHD changes that.

---

## What It Does

MORPHD Personal Intelligence ingests a user's portable personal data and generates a **Weekly Intelligence Report** containing:

- **Decision Pattern Analysis** — When do you make your best decisions? When are you most depleted and most at risk of reactive choices?
- **Behavioral Loop Detection** — What recurring patterns are driving outcomes you haven't consciously connected yet?
- **Capacity & Recovery Mapping** — How does your physical state (sleep, HRV) correlate with your cognitive output and emotional tone?
- **Strategic Momentum Score** — A composite weekly read on whether you're operating in growth mode or survival mode

The insight is non-obvious. The framing is human. The value flows entirely to the user.

---

## Demo Persona: Darius Webb

For this hackathon submission, MORPHD Personal Intelligence is demonstrated using **p03 — Darius Webb**, the synthetic persona provided by the Data Transfer Initiative:

- 41-year-old agency founder, Austin TX
- Navigating post-divorce rebuild, co-parenting, and scaling his business simultaneously
- Data includes: AI conversation history, lifelog, emails, calendar, transactions, social posts

Darius is the prototypical MORPHD user: high-functioning, data-rich, insight-poor. His weekly intelligence report surfaces patterns he couldn't see from inside the grind.

---

## Architecture

```
data/
  └── personas/
        └── p03_darius_webb/     # DTI synthetic persona data
              ├── conversations.json
              ├── lifelog.json
              ├── calendar.json
              ├── transactions.json
              └── social_posts.json

src/
  ├── ingest/
  │     └── normalizer.py        # Parses and normalizes multi-source data
  ├── agent/
  │     ├── graph.py             # LangGraph orchestration layer
  │     ├── nodes.py             # Agent nodes: analyze, pattern_detect, synthesize
  │     └── prompts.py           # Intelligence prompting layer
  ├── output/
  │     └── report_generator.py  # Formats Weekly Intelligence Report
  └── main.py                    # Entry point

reports/
  └── darius_webb_week1.md       # Sample output report
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Agent Orchestration | LangGraph |
| Language Model | Claude (Anthropic) |
| Data Normalization | Python / Pandas |
| Pattern Analysis | Custom behavioral analysis pipeline |
| Output | Markdown report + structured JSON |

---

## Quickstart

```bash
# Clone the repo
git clone https://github.com/morphd-ai/morphd-companion-demo.git
cd morphd-companion-demo

# Install dependencies
pip install -r requirements.txt

# Add your Anthropic API key
cp .env.example .env
# Edit .env and add: ANTHROPIC_API_KEY=your_key_here

# Run the intelligence agent on the demo persona
python src/main.py --persona p03_darius_webb
```

The agent will process the persona data and generate a Weekly Intelligence Report in `/reports/`.

---

## Sample Output

```
MORPHD WEEKLY INTELLIGENCE REPORT
Persona: Darius Webb | Week of March 2, 2026
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DECISION PATTERN ANALYSIS
Your highest-leverage decisions this week occurred Tuesday and Wednesday
before 11am. Three significant reactive decisions were made after 9pm —
all following days with under 6 hours of sleep.

BEHAVIORAL LOOP DETECTED
A recurring pattern across 6 weeks: client conflict → late-night venting
in AI conversations → next-day procrastination on business development.
This loop has appeared 4 times in the last 6 weeks.

CAPACITY SCORE: 6.2 / 10
You are operating in yellow zone. Strategic work is possible but at
reduced bandwidth. Recommend protecting morning hours and deferring
high-stakes conversations until Wednesday.

STRATEGIC MOMENTUM: REBUILDING ↗
Evidence of intentional forward motion despite significant personal load.
You are not in survival mode — but you are close to the edge.
```

---

## About MORPHD

MORPHD is a Personal Intelligence Infrastructure platform built on 10+ years of longitudinal strategic intelligence data. It was founded by **Bren Bauer**, a Licensed Executive Coach and TensorFlow-Certified AI Developer, who built MORPHD as her own personal optimization system before recognizing its potential for high-performing executives.

MORPHD's production architecture includes LangGraph orchestration, LSTM neural networks, Neo4j knowledge graphs, Prophet forecasting, and Whoop biometric integration.

This hackathon submission is a focused demonstration of MORPHD's intelligence layer — built on open, portable personal data that belongs entirely to the user.

**Contact:** bren@morphd.ai | [morphd.ai](https://morphd.ai)

---

## Hackathon Submission

- **Track:** Track 2 — AI Companions with Purpose
- **Submitted by:** Bren Bauer, Founder & CEO, MORPHD
- **Deadline:** March 9, 2026, 10pm CT
- **Event:** Data Portability Hackathon 2026, Austin TX

---

*MORPHD: Your data. Your intelligence. Your terms.*
