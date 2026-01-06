import duckdb
from pathlib import Path

DB_PATH = Path(__file__).parent / "warehouse.duckdb"

con = duckdb.connect(DB_PATH)

print("📊 Row counts:")

for table in ["fact_claims", "dim_member", "dim_provider", "dim_date"]:
    result = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
    print(f"{table}: {result[0]}")

print("\n📈 Sample query (denials by month):")

query = """
SELECT
    d.year,
    d.month,
    COUNT(*) AS total_claims,
    SUM(f.denial_flag) AS denied_claims
FROM fact_claims f
JOIN dim_date d
    ON f.service_date = d.date
GROUP BY d.year, d.month
ORDER BY d.year, d.month
"""

df = con.execute(query).df()
print(df)

con.close()
