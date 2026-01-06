# 🧠 AI-Powered Data Warehouse Copilot

An **AI-ready analytics copilot** that allows users to ask business questions in plain English and automatically generates **safe SQL**, executes it on a data warehouse, and returns **smart visualizations** (line charts and heatmaps).

Built with **Python, DuckDB, Streamlit**, and a **fault-tolerant LLM integration**.

## 🚀 Key Features

- 💬 Ask analytics questions in **natural language**
- 🔍 Metadata-driven table discovery
- 🧠 Deterministic query planning (no unsafe SQL)
- 🧾 Guard-railed SQL generation
- 📊 Automatic visualization selection:
  - Line charts for time-based trends
  - Heatmaps for multi-dimensional analysis
- 🤖 **LLM-ready architecture with safe fallback**
- 🌐 Interactive Streamlit web UI
- ⬇️ Download query results as CSV

---

## 🏗️ Architecture Overview

User Question
↓
(Optional) LLM Intent Normalization
↓
Metadata Catalog Search
↓
Query Planner
↓
SQL Generator (Guard-railed)
↓
DuckDB Execution
↓
Smart Visualization (Line / Heatmap)

yaml

### 🔐 Safety by Design
- LLMs **never generate SQL**
- SQL is fully deterministic
- Warehouse access is tightly controlled
- If the LLM is unavailable, the system **gracefully falls back**

---

## 📊 Example Questions

denied claims by month
claims by provider specialty and month
denied claims by state and month

---

## 📈 Visualization Examples

- 📈 **Line Chart** – Time-based trend analysis  
- 🔥 **Heatmap** – Two-dimensional insights (e.g., specialty × month)

---

## 🧪 Tech Stack

- Python
- DuckDB
- Streamlit
- Plotly
- Metadata-driven query planning
- LLM-ready (optional OpenAI integration)

---

## ▶️ How to Run Locally

```bash
conda activate warehousecopilot
cd llm-warehouse-copilot
streamlit run app/app.py

🤖 About the AI Layer
The system includes an optional LLM layer for intent normalization.

If an API key is configured → AI enhances the question

If not → system falls back to deterministic logic

This design ensures reliability, safety, and production readiness.
