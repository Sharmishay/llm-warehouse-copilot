def generate_sql(query_plan):
    """
    Convert a query plan into SAFE SQL.
    Guardrails:
    - SELECT is never empty
    - ORDER BY only when columns exist
    """

    table = query_plan["table"]
    group_by = query_plan.get("group_by", [])
    metrics = query_plan.get("metrics", [])

    select_parts = []
    group_parts = []

    # Time dimensions
    if "year" in group_by:
        select_parts.append("d.year")
        group_parts.append("d.year")

    if "month" in group_by:
        select_parts.append("d.month")
        group_parts.append("d.month")

    # Metrics
    if "denial_flag" in metrics:
        select_parts.append("SUM(f.denial_flag) AS denied_claims")
        select_parts.append("COUNT(*) AS total_claims")

    # 🚨 GUARDRAIL: fallback if nothing selected
    if not select_parts:
        select_parts.append("COUNT(*) AS total_claims")

    sql = f"""
    SELECT
        {", ".join(select_parts)}
    FROM fact_claims f
    JOIN dim_date d
        ON f.service_date = d.date
    """

    if group_parts:
        sql += f"\nGROUP BY {', '.join(group_parts)}"
        sql += f"\nORDER BY {', '.join(group_parts)}"

    return sql.strip()


if __name__ == "__main__":
    # Simulated query plan (from previous step)
    query_plan = {
        "table": "fact_claims",
        "group_by": ["year", "month"],
        "metrics": ["denial_flag"]
    }

    sql = generate_sql(query_plan)

    print("🧾 Generated SQL:\n")
    print(sql)
