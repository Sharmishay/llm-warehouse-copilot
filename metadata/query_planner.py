import json
from pathlib import Path

CATALOG_PATH = Path(__file__).parent / "metadata.json"


def load_catalog():
    with open(CATALOG_PATH, "r") as f:
        return json.load(f)


def plan_query(user_query, catalog, selected_tables):
    """
    Create a simple query plan:
    - which table
    - which columns
    - what operation (aggregation or not)
    - grouping keys
    """
    query = user_query.lower()

    plan = {
        "table": None,
        "columns": [],
        "group_by": [],
        "metrics": []
    }

    # Pick the top table
    # Always prefer fact table if present
    fact_table = next((t for t in selected_tables if "fact" in t["table"]), None)
    plan["table"] = fact_table["table"] if fact_table else selected_tables[0]["table"]


    # Simple rules (this is intentional and GOOD)
    if "denied" in query or "denial" in query:
        plan["metrics"].append("denial_flag")

    if "month" in query or "monthly" in query:
        plan["group_by"].append("month")
        plan["group_by"].append("year")

    if "member" in query:
        plan["group_by"].append("member_id")

    if "provider" in query:
        plan["group_by"].append("provider_id")

    return plan


if __name__ == "__main__":
    catalog = load_catalog()

    # Simulate output from catalog search
    selected_tables = [
        {"table": "fact_claims"}
    ]

    user_question = input("🧠 Enter your question: ")

    query_plan = plan_query(user_question, catalog, selected_tables)

    print("\n🧩 Query Plan:")
    for k, v in query_plan.items():
        print(f"{k}: {v}")
