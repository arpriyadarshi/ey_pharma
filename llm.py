import json
from typing import List, Dict, Any
from utils import make_json_serializable

from openai import OpenAI
import streamlit as st

from schemas import StructuredQuery
from prompts import (
    QUERY_PARSER_PROMPT,
    AGENT_ROUTER_PROMPT,
    REPORT_GENERATION_PROMPT
)

# Load environment variables
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)


# -------------------------------------------------
# Helper: Safe JSON Parse
# -------------------------------------------------
def _safe_json_loads(text: str) -> Dict[str, Any]:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON returned by LLM:\n{text}")


# -------------------------------------------------
# Step 1: Parse User Query
# -------------------------------------------------
def parse_query_with_llm(user_query: str) -> StructuredQuery:
    """
    Extracts structured fields from user query using LLM.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": QUERY_PARSER_PROMPT},
            {"role": "user", "content": user_query}
        ],
        temperature=0
    )

    content = response.choices[0].message.content
    parsed_json = _safe_json_loads(content)

    return StructuredQuery(**parsed_json)


# -------------------------------------------------
# Step 2: Agent Routing
# -------------------------------------------------
def route_agents_with_llm(
    user_query: str,
    structured_query: StructuredQuery,
    has_internal_docs: bool
) -> List[str]:
    """
    Decides which worker agents to call.
    """
    input_payload = {
        "user_query": user_query,
        "structured_query": structured_query.model_dump(),
        "has_internal_docs": has_internal_docs
    }

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": AGENT_ROUTER_PROMPT},
            {"role": "user", "content": json.dumps(input_payload)}
        ],
        temperature=0
    )

    content = response.choices[0].message.content
    parsed_json = _safe_json_loads(content)

    return parsed_json.get("agents", [])


# -------------------------------------------------
# Step 4: Report Generation
# -------------------------------------------------
def generate_report_with_llm(
    user_query: str,
    structured_query: StructuredQuery,
    agent_outputs: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Generates final analytical report using LLM.
    """
    input_payload = {
    "user_query": user_query,
    "structured_query": structured_query.model_dump(),
    "agent_outputs": make_json_serializable(agent_outputs)
    }

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": REPORT_GENERATION_PROMPT},
            {"role": "user", "content": json.dumps(input_payload)}
        ],
        temperature=0.2
    )

    content = response.choices[0].message.content
    return _safe_json_loads(content)
