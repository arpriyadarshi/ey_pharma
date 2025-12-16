import streamlit as st
import pandas as pd

from orchestrator import run_pipeline


# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Pharma Agentic Intelligence",
    layout="wide"
)

st.title("🧠 Pharma Agentic Intelligence Platform")
st.caption(
    "Agent-based analysis of pharma strategy queries using clinical, market, patent, and trade intelligence."
)

st.divider()

# -----------------------------
# User Inputs
# -----------------------------
st.subheader("🔍 Enter Your Query")

query = st.text_area(
    label="Pharma Strategy Question",
    placeholder="e.g. Is there commercial potential for a new oncology drug in India using pembrolizumab?",
    height=120
)

uploaded_docs = st.file_uploader(
    "Upload internal documents (optional)",
    type=["pdf", "txt"],
    accept_multiple_files=True
)

analyze_btn = st.button("🚀 Analyze", use_container_width=True)

st.divider()

# -----------------------------
# Run Pipeline
# -----------------------------
if analyze_btn:
    if not query.strip():
        st.warning("Please enter a query before running the analysis.")
    else:
        with st.spinner("Running agentic analysis..."):
            try:
                report = run_pipeline(
                    query=query,
                    uploaded_docs=uploaded_docs
                )
            except Exception as e:
                st.error("An error occurred while running the analysis.")
                st.exception(e)
                st.stop()

        # -----------------------------
        # Render Report
        # -----------------------------
        st.success("Analysis completed successfully.")

        # Executive Summary
        st.subheader("📌 Executive Summary")
        st.write(report.get("executive_summary", "No summary generated."))

        st.divider()

        # Sections
        sections = report.get("sections", [])
        for section in sections:
            st.subheader(section.get("title", "Section"))

            if "insights" in section:
                st.write(section["insights"])

            # Tables
            tables = section.get("tables", [])
            for table in tables:
                if isinstance(table, list):
                    st.table(pd.DataFrame(table))

            # Charts
            # Charts
            charts = section.get("charts", [])
            for chart in charts:
                chart_type = chart.get("type")
                data = chart.get("data")

                # Ensure data is a dictionary like {label: value}
                if not data or not isinstance(data, dict):
                    continue

                # Convert dict -> DataFrame correctly
                df = pd.DataFrame(
                    list(data.items()),
                    columns=["Category", "Value"]
                )

                df = df.set_index("Category")

                if chart_type == "bar":
                    st.bar_chart(df)

                elif chart_type == "line":
                    st.line_chart(df)


            st.divider()

        # Final Recommendation
        if "final_recommendation" in report:
            st.subheader("✅ Final Recommendation")
            st.write(report["final_recommendation"])
