import pandas as pd
from typing import Dict, Any, List

from schemas import StructuredQuery
from utils import load_csv_safe


# -------------------------------------------------
# Clinical Trials Agent
# -------------------------------------------------
def clinical_trials_agent(query: StructuredQuery) -> Dict[str, Any]:
    """
    Analyzes competitive pipeline using clinical trials data.
    """
    df = load_csv_safe("data/clinical_trials.csv")

    if query.disease:
        df = df[df["disease"].str.contains(query.disease, case=False, na=False)]

    if query.molecule:
        df = df[df["molecule"].str.contains(query.molecule, case=False, na=False)]

    result = {
        "total_trials": len(df),
        "phase_distribution": df["phase"].value_counts().to_dict(),
        "top_sponsors": df["sponsor"].value_counts().head(5).to_dict()
    }

    return result


# -------------------------------------------------
# IQVIA Market Insights Agent
# -------------------------------------------------
def iqvia_agent(query: StructuredQuery) -> Dict[str, Any]:
    """
    Provides commercial viability analysis using market data.
    """
    df = load_csv_safe("data/iqvia_market.csv")

    if query.country:
        df = df[df["country"].str.contains(query.country, case=False, na=False)]

    if query.disease:
        df = df[df["disease"].str.contains(query.disease, case=False, na=False)]

    result = {
        "market_size_usd_mn": df["market_size_usd_mn"].sum(),
        "cagr_percent_avg": round(df["cagr_percent"].mean(), 2) if not df.empty else 0,
        "key_players": df["company"].value_counts().head(5).to_dict()
    }

    return result


# -------------------------------------------------
# Patent Landscape Agent
# -------------------------------------------------
def patent_landscape_agent(query: StructuredQuery) -> Dict[str, Any]:
    """
    Assesses IP risk using patent filings data.
    """
    df = load_csv_safe("data/patents.csv")

    if query.molecule:
        df = df[df["molecule"].str.contains(query.molecule, case=False, na=False)]

    if query.country:
        df = df[df["jurisdiction"].str.contains(query.country, case=False, na=False)]

    result = {
        "total_patents": len(df),
        "active_patents": int(df["status"].str.contains("active", case=False).sum()),
        "top_assignees": df["assignee"].value_counts().head(5).to_dict()
    }

    return result


# -------------------------------------------------
# EXIM Trade Trends Agent
# -------------------------------------------------
def exim_trends_agent(query: StructuredQuery) -> Dict[str, Any]:
    """
    Analyzes export-import trends for supply chain stability.
    """
    df = load_csv_safe("data/exim_trade.csv")

    if query.country:
        df = df[df["country"].str.contains(query.country, case=False, na=False)]

    result = {
        "total_trade_value_usd_mn": df["trade_value_usd_mn"].sum(),
        "top_trade_partners": df["partner_country"].value_counts().head(5).to_dict()
    }

    return result


# -------------------------------------------------
# Web Intelligence Agent (Simulated)
# -------------------------------------------------
def web_intelligence_agent(query: StructuredQuery) -> Dict[str, Any]:
    """
    Simulated external scientific rationale.
    """
    insights: List[str] = []

    if query.disease:
        insights.append(f"Recent publications indicate increasing research activity in {query.disease}.")

    if query.molecule:
        insights.append(f"{query.molecule} has shown promising results in late-stage trials.")

    return {
        "key_insights": insights or ["No significant external signals detected."]
    }


# -------------------------------------------------
# Internal Knowledge Agent
# -------------------------------------------------
def internal_knowledge_agent(
    query: StructuredQuery,
    uploaded_docs: List[Any]
) -> Dict[str, Any]:
    """
    Summarizes uploaded internal documents (basic placeholder).
    """
    doc_names = [doc.name for doc in uploaded_docs]

    return {
        "documents_analyzed": len(uploaded_docs),
        "document_names": doc_names,
        "summary": "Internal documents reviewed for strategic alignment."
    }
