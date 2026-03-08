"""LangGraph orchestration for the MORPHD intelligence pipeline."""

from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph

from src.agent.nodes import analyze_domains, detect_patterns, synthesize_report


class AgentState(TypedDict):
    persona_data: dict[str, Any]
    domain_analysis: str
    patterns: str
    report_content: str


def build_graph() -> StateGraph:
    """Build and compile the 3-stage intelligence pipeline.

    Flow: analyze_domains → detect_patterns → synthesize_report
    """
    graph = StateGraph(AgentState)

    graph.add_node("analyze_domains", analyze_domains)
    graph.add_node("detect_patterns", detect_patterns)
    graph.add_node("synthesize_report", synthesize_report)

    graph.add_edge(START, "analyze_domains")
    graph.add_edge("analyze_domains", "detect_patterns")
    graph.add_edge("detect_patterns", "synthesize_report")
    graph.add_edge("synthesize_report", END)

    return graph.compile()
