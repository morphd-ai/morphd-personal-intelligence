"""Ingest and normalize multi-source persona data from JSONL/JSON files."""

import json
import logging
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def load_consent(data_dir: Path) -> dict:
    """Read and log consent settings from consent.json in data_dir.

    Returns the consent dict, or an empty dict if the file is missing.
    """
    consent_path = Path(data_dir) / "consent.json"
    if not consent_path.exists():
        logger.warning("No consent.json found at %s", consent_path)
        print("[CONSENT] WARNING: No consent.json found. Proceeding without consent verification.")
        return {}

    with open(consent_path, encoding="utf-8") as f:
        consent = json.load(f)

    allowed = ", ".join(consent.get("allowed_uses", []))
    prohibited = ", ".join(consent.get("prohibited_uses", []))
    retention = consent.get("retention", "unspecified")
    dataset_type = consent.get("dataset_type", "unspecified")
    persona_id = consent.get("persona_id", "unknown")

    logger.info("Consent loaded for persona_id=%s dataset_type=%s", persona_id, dataset_type)
    logger.info("Allowed uses: %s", allowed)
    logger.info("Prohibited uses: %s", prohibited)
    logger.info("Retention policy: %s", retention)

    print("[CONSENT] Consent settings loaded")
    print(f"  Persona ID   : {persona_id}")
    print(f"  Dataset type : {dataset_type}")
    print(f"  Allowed uses : {allowed}")
    print(f"  Prohibited   : {prohibited}")
    print(f"  Retention    : {retention}")
    if consent.get("notes"):
        print(f"  Notes        : {consent['notes']}")
    print("[CONSENT] Proceeding with pipeline run.\n")

    return consent


def _load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _load_jsonl(path: Path) -> list[dict]:
    records = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def _parse_timestamp(ts_str: str) -> datetime:
    return datetime.fromisoformat(ts_str)


def _iso_week_key(dt: datetime) -> str:
    iso = dt.isocalendar()
    return f"{iso[0]}-W{iso[1]:02d}"


def _parse_transaction(text: str) -> dict[str, Any]:
    """Extract amount, description, and category from transaction text.

    Format: '$X.XX - description - category'
    """
    parts = text.split(" - ", 2)
    result: dict[str, Any] = {"raw": text}
    if len(parts) >= 1:
        amount_str = parts[0].replace("$", "").replace(",", "")
        try:
            result["amount"] = float(amount_str)
        except ValueError:
            result["amount"] = 0.0
    if len(parts) >= 2:
        result["description"] = parts[1]
    if len(parts) >= 3:
        result["category"] = parts[2]
    return result


def _deduplicate(records: list[dict]) -> list[dict]:
    """Remove duplicate records by (source, text) keeping the earliest occurrence."""
    seen: set[tuple[str, str]] = set()
    unique = []
    for r in records:
        key = (r.get("source", ""), r.get("text", ""))
        if key not in seen:
            seen.add(key)
            unique.append(r)
    return unique


def load_persona_data(data_dir: Path) -> dict[str, Any]:
    """Load, normalize, and structure all persona data files.

    Returns a dict with:
        profile:    persona profile dict
        records:    all records sorted chronologically (deduplicated)
        by_source:  records grouped by source type
        by_week:    records grouped by ISO week
        by_tags:    records grouped by tag
        summary:    record counts and date range metadata
    """
    data_dir = Path(data_dir)

    # Read and log consent settings before processing any data
    load_consent(data_dir)

    # Load profile
    profile = _load_json(data_dir / "persona_profile.json")

    # Load all JSONL sources
    source_files = {
        "lifelog": "lifelog.jsonl",
        "calendar": "calendar.jsonl",
        "conversations": "conversations.jsonl",
        "emails": "emails.jsonl",
        "transactions": "transactions.jsonl",
        "social_posts": "social_posts.jsonl",
        "files_index": "files_index.jsonl",
    }

    all_records: list[dict] = []
    for source_name, filename in source_files.items():
        filepath = data_dir / filename
        if filepath.exists():
            records = _load_jsonl(filepath)
            all_records.extend(records)

    # Parse timestamps
    for record in all_records:
        record["_dt"] = _parse_timestamp(record["ts"])
        record["_week"] = _iso_week_key(record["_dt"])

    # Enrich transactions with parsed amounts
    for record in all_records:
        if record.get("source") == "bank":
            record["_transaction"] = _parse_transaction(record["text"])

    # Deduplicate
    all_records = _deduplicate(all_records)

    # Sort chronologically
    all_records.sort(key=lambda r: r["_dt"])

    # Group by source
    by_source: dict[str, list[dict]] = defaultdict(list)
    for r in all_records:
        by_source[r["source"]].append(r)

    # Group by week
    by_week: dict[str, list[dict]] = defaultdict(list)
    for r in all_records:
        by_week[r["_week"]].append(r)

    # Group by tag
    by_tags: dict[str, list[dict]] = defaultdict(list)
    for r in all_records:
        for tag in r.get("tags", []):
            by_tags[tag].append(r)

    # Summary stats
    timestamps = [r["_dt"] for r in all_records]
    summary = {
        "total_records": len(all_records),
        "unique_weeks": len(by_week),
        "date_range_start": min(timestamps).isoformat() if timestamps else None,
        "date_range_end": max(timestamps).isoformat() if timestamps else None,
        "records_per_source": {k: len(v) for k, v in by_source.items()},
    }

    return {
        "profile": profile,
        "records": all_records,
        "by_source": dict(by_source),
        "by_week": dict(by_week),
        "by_tags": dict(by_tags),
        "summary": summary,
    }


def serialize_for_llm(persona_data: dict[str, Any]) -> str:
    """Serialize persona data into a text block for LLM consumption.

    Converts the structured data into a readable narrative format that
    fits within context windows while preserving analytical richness.
    """
    lines: list[str] = []
    profile = persona_data["profile"]

    # Profile section
    lines.append("=" * 60)
    lines.append("PERSONA PROFILE")
    lines.append("=" * 60)
    lines.append(f"Name: {profile['name']}")
    lines.append(f"Age: {profile['age']} | Location: {profile['location']}")
    lines.append(f"Role: {profile['job']} at {profile['employer']}")
    lines.append(f"Household: {profile['household']}")
    lines.append(f"Income: {profile['income_approx']}")
    lines.append(f"Goals: {'; '.join(profile['goals'])}")
    lines.append(f"Pain points: {'; '.join(profile['pain_points'])}")
    lines.append(f"Strengths: {', '.join(profile['personality']['strengths'])}")
    lines.append(f"Growth areas: {', '.join(profile['personality']['growth_areas'])}")
    lines.append(f"AI tone preference: {profile['personality']['ai_assistant_tone']}")
    lines.append("")

    # Data summary
    summary = persona_data["summary"]
    lines.append("=" * 60)
    lines.append("DATA OVERVIEW")
    lines.append("=" * 60)
    lines.append(f"Total records: {summary['total_records']}")
    lines.append(f"Date range: {summary['date_range_start']} to {summary['date_range_end']}")
    lines.append(f"Weeks covered: {summary['unique_weeks']}")
    for source, count in summary["records_per_source"].items():
        lines.append(f"  {source}: {count} records")
    lines.append("")

    # Records by source
    source_labels = {
        "lifelog": "LIFELOG (Reflections & Activities)",
        "ai_chat": "AI CONVERSATIONS",
        "email": "EMAILS",
        "calendar": "CALENDAR",
        "bank": "TRANSACTIONS",
        "social": "SOCIAL POSTS",
        "files": "FILES INDEX",
    }

    for source_key, label in source_labels.items():
        records = persona_data["by_source"].get(source_key, [])
        if not records:
            continue
        lines.append("-" * 60)
        lines.append(f"{label} ({len(records)} records)")
        lines.append("-" * 60)
        for r in records:
            ts_short = r["_dt"].strftime("%Y-%m-%d %a")
            tags_str = ", ".join(r.get("tags", []))
            rtype = r.get("type", "")
            lines.append(f"[{ts_short}] ({rtype}) {r['text']}")
            if tags_str:
                lines.append(f"  tags: {tags_str}")
        lines.append("")

    return "\n".join(lines)
