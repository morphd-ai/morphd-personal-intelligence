"""LangGraph node functions for the MORPHD intelligence pipeline."""

from typing import Any

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage

from src.agent.prompts import (
    DOMAIN_ANALYSIS_PROMPT,
    PATTERN_DETECTION_PROMPT,
    SYNTHESIS_PROMPT,
)
from src.ingest.normalizer import serialize_for_llm


def _get_llm() -> ChatAnthropic:
    return ChatAnthropic(
        model="claude-sonnet-4-5-20250929",
        max_tokens=8192,
        temperature=0.3,
    )


def _profile_field(state: dict[str, Any], field: str, default: str = "") -> str:
    return state["persona_data"]["profile"].get(field, default)


def analyze_domains(state: dict[str, Any]) -> dict[str, Any]:
    """Analyze each life domain from the longitudinal data."""
    llm = _get_llm()
    persona_text = serialize_for_llm(state["persona_data"])
    profile = state["persona_data"]["profile"]

    prompt = DOMAIN_ANALYSIS_PROMPT.format(
        name=profile["name"],
        age=profile["age"],
        job=profile["job"],
        location=profile["location"],
        persona_data=persona_text,
    )

    response = llm.invoke([HumanMessage(content=prompt)])
    return {"domain_analysis": response.content}


def detect_patterns(state: dict[str, Any]) -> dict[str, Any]:
    """Detect cross-domain behavioral patterns."""
    llm = _get_llm()
    persona_text = serialize_for_llm(state["persona_data"])
    profile = state["persona_data"]["profile"]

    prompt = PATTERN_DETECTION_PROMPT.format(
        name=profile["name"],
        domain_analysis=state["domain_analysis"],
        persona_data=persona_text,
    )

    response = llm.invoke([HumanMessage(content=prompt)])
    return {"patterns": response.content}


def synthesize_report(state: dict[str, Any]) -> dict[str, Any]:
    """Synthesize the final Weekly Intelligence Report."""
    llm = _get_llm()
    persona_text = serialize_for_llm(state["persona_data"])
    profile = state["persona_data"]["profile"]
    summary = state["persona_data"]["summary"]

    report_period = f"{summary['date_range_start'][:10]} to {summary['date_range_end'][:10]}"

    prompt = SYNTHESIS_PROMPT.format(
        name=profile["name"],
        report_period=report_period,
        domain_analysis=state["domain_analysis"],
        patterns=state["patterns"],
        persona_data=persona_text,
    )

    response = llm.invoke([HumanMessage(content=prompt)])
    return {"report_content": response.content}
