import duckdb
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "warehouse" / "warehouse.duckdb"


def execute_sql(sql):
    con = duckdb.connect(DB_PATH)
    df = con.execute(sql).df()
    con.close()
    return df


if __name__ == "__main__":
    # SQL generated from previous step
    sql = """
    SELECT
        d.year,
        d.month,
        SUM(f.denial_flag) AS denied_claims,
        COUNT(*) AS total_claims
    FROM fact_claims f
    JOIN dim_date d
        ON f.service_date = d.date
    GROUP BY d.year, d.month
    ORDER BY d.year, d.month
    """

    print("🚀 Executing SQL...\n")
    result_df = execute_sql(sql)

    print(result_df)
