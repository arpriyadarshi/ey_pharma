from pydantic import BaseModel, Field
from typing import Dict, List, Any


# -------------------------------------------------
# Structured Query Schema
# -------------------------------------------------
class StructuredQuery(BaseModel):
    """
    Parsed representation of the user query.
    Empty strings are allowed when fields are not present.
    """
    disease: str = Field(default="", description="Disease or therapeutic area")
    country: str = Field(default="", description="Target country or region")
    molecule: str = Field(default="", description="Drug or molecule name")


# -------------------------------------------------
# Agent Routing Output Schema (Optional but useful)
# -------------------------------------------------
class AgentRoutingResult(BaseModel):
    agents: List[str]


# -------------------------------------------------
# Final Report Schema (Reference)
# -------------------------------------------------
class ReportSection(BaseModel):
    title: str
    insights: str
    tables: List[List[Dict[str, Any]]] = []
    charts: List[Dict[str, Any]] = []


class FinalReport(BaseModel):
    executive_summary: str
    sections: List[ReportSection]
    final_recommendation: str
