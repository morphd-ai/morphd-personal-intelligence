"""MORPHD Personal Intelligence — Entry Point

Ingests a synthetic persona's longitudinal data and generates a
Weekly Intelligence Report surfacing behavioral patterns and
decision intelligence.
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Ensure project root is on sys.path so `src.*` imports work when run directly
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

PERSONA_ID = "p03_darius_webb"
DATA_DIR = PROJECT_ROOT / "data" / "personas" / PERSONA_ID
REPORTS_DIR = PROJECT_ROOT / "reports"


def main() -> None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY is not set. Copy .env.example to .env and add your key."
        )

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("MORPHD Personal Intelligence")
    print("=" * 60)

    # 1. Ingest & normalize persona data
    from src.ingest.normalizer import load_persona_data

    print("\n[1/4] Loading persona data...")
    persona_data = load_persona_data(DATA_DIR)
    summary = persona_data["summary"]
    print(f"      Loaded {summary['total_records']} records across {summary['unique_weeks']} weeks")
    print(f"      Sources: {summary['records_per_source']}")

    # 2. Run the LangGraph intelligence agent
    from src.agent.graph import build_graph

    print("\n[2/4] Analyzing life domains...")
    graph = build_graph()
    result = graph.invoke({"persona_data": persona_data})
    print("      Domain analysis complete.")

    print("\n[3/4] Detecting cross-domain patterns...")
    print("      Pattern detection complete.")

    # 3. Generate the Weekly Intelligence Report
    from src.output.report_generator import generate_report

    print("\n[4/4] Generating Weekly Intelligence Report...")
    report_path = generate_report(result, REPORTS_DIR, PERSONA_ID)

    print(f"\n{'=' * 60}")
    print(f"Report written to: {report_path}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
