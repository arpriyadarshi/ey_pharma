from typing import List, Optional, Dict, Any

from llm import (
    parse_query_with_llm,
    route_agents_with_llm,
    generate_report_with_llm
)
from agents import (
    clinical_trials_agent,
    iqvia_agent,
    patent_landscape_agent,
    exim_trends_agent,
    web_intelligence_agent,
    internal_knowledge_agent
)
from schemas import StructuredQuery


# -------------------------------------------------
# Main Pipeline
# -------------------------------------------------
def run_pipeline(
    query: str,
    uploaded_docs: Optional[List[Any]] = None
) -> Dict[str, Any]:
    """
    Orchestrates the full agentic analysis pipeline.

    Steps:
    1. Parse user query into structured JSON
    2. Decide which worker agents to run
    3. Run selected worker agents (deterministic)
    4. Generate final report using LLM

    Returns:
        Final structured report dictionary
    """

    # -----------------------------
    # Step 1: Parse Query
    # -----------------------------
    structured_query: StructuredQuery = parse_query_with_llm(query)

    # -----------------------------
    # Step 2: Decide Agents
    # -----------------------------
    selected_agents: List[str] = route_agents_with_llm(
        user_query=query,
        structured_query=structured_query,
        has_internal_docs=bool(uploaded_docs)
    )

    # -----------------------------
    # Step 3: Run Worker Agents
    # -----------------------------
    agent_outputs: Dict[str, Any] = {}

    for agent_name in selected_agents:
        if agent_name == "ClinicalTrialsAgent":
            agent_outputs["clinical_trials"] = clinical_trials_agent(structured_query)

        elif agent_name == "IQVIAInsightsAgent":
            agent_outputs["iqvia_insights"] = iqvia_agent(structured_query)

        elif agent_name == "PatentLandscapeAgent":
            agent_outputs["patent_landscape"] = patent_landscape_agent(structured_query)

        elif agent_name == "EXIMTrendsAgent":
            agent_outputs["exim_trends"] = exim_trends_agent(structured_query)

        elif agent_name == "WebIntelligenceAgent":
            agent_outputs["web_intelligence"] = web_intelligence_agent(structured_query)

        elif agent_name == "InternalKnowledgeAgent" and uploaded_docs:
            agent_outputs["internal_knowledge"] = internal_knowledge_agent(
                structured_query,
                uploaded_docs
            )

    # -----------------------------
    # Step 4: Generate Final Report
    # -----------------------------
    final_report: Dict[str, Any] = generate_report_with_llm(
        user_query=query,
        structured_query=structured_query,
        agent_outputs=agent_outputs
    )

    return final_report
