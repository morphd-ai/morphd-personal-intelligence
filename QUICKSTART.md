# MORPHD Personal Intelligence — Quickstart

## Prerequisites

- Python 3.11+
- An [Anthropic API key](https://console.anthropic.com/)

## Run It

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Add your API key
cp .env.example .env
# Edit .env and set ANTHROPIC_API_KEY=sk-ant-...

# 3. Run the pipeline
python src/main.py
```

Your report will be generated in `reports/`.

## What Happens

The pipeline ingests Darius Webb's longitudinal data (lifelog, calendar, transactions, emails, conversations, social posts) and runs a 3-stage LangGraph analysis:

1. **Domain Analysis** — Health, Business, Parenting, Emotional, Creative
2. **Pattern Detection** — Cross-domain correlations (recovery→decisions, custody→productivity, avoidance signatures)
3. **Report Synthesis** — Weekly Intelligence Report with actionable prescriptions

Total runtime: ~45 seconds, 3 Claude API calls.
