import sys
from pathlib import Path

# Add project root to Python path (MUST be first)
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from llm.llm_helper import enhance_question


import streamlit as st
import pandas as pd

from metadata.search_catalog import search_catalog, load_catalog
from metadata.query_planner import plan_query
from metadata.sql_generator import generate_sql
from metadata.sql_executor import execute_sql
from metadata.visualizer import visualize

st.set_page_config(page_title="LLM Warehouse Copilot", layout="wide")

st.title("🧠 AI-Powered Data Warehouse Copilot")
st.markdown(
    """
    Ask business questions in **plain English** and get:
    - 📊 Query results
    - 🧾 Safe SQL
    - 📈 Smart visualizations (Line charts & Heatmaps)

    Built with **DuckDB, Python, and AI-ready guardrails**.
    """
)

col1, col2 = st.columns([4, 1])

with col1:
    user_question = st.text_input(
        "💬 Ask a data question",
        placeholder="e.g. denied claims by month"
    )

with col2:
    if st.button("🔄 Reset"):
        st.experimental_rerun()

if user_question:
    st.divider()

    # 🤖 LLM interpretation
    enhanced_question = enhance_question(user_question)

    st.subheader("🤖 AI Interpretation")
    st.info(enhanced_question)

    # 1. Load catalog
    catalog = load_catalog()

    # 2. Search tables
    search_results = search_catalog(enhanced_question, catalog)


    if not search_results:
        st.error("No relevant tables found.")
        st.stop()

    st.subheader("🔍 Relevant Tables")
    for r in search_results:
        st.write(f"• **{r['table']}** (score={r['score']})")

    # 3. Query planning
    query_plan = plan_query(enhanced_question, catalog, search_results)

    st.subheader("🧠 Query Plan")
    st.json(query_plan)

    # 4. SQL generation
    sql = generate_sql(query_plan)

    st.subheader("🧾 Generated SQL")
    st.code(sql, language="sql")

    # 5. SQL execution
    df = execute_sql(sql)

    st.subheader("📊 Query Results")
    st.dataframe(df)

    st.download_button(
    label="⬇️ Download results as CSV",
    data=df.to_csv(index=False),
    file_name="query_results.csv",
    mime="text/csv"
)

# 6. Visualization
    st.subheader("📈 Visualization")

    if df.shape[1] >= 3:
        st.info("Chart type: 🔥 Heatmap (2-dimensional analysis)")
    else:
        st.info("Chart type: 📈 Line chart (trend analysis)")

    visualize(df)


