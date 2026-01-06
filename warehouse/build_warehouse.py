import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "sample_data"
DB_PATH = BASE_DIR / "warehouse.duckdb"

con = duckdb.connect(DB_PATH)

# Load dimension tables
con.execute(f"""
    CREATE OR REPLACE TABLE dim_date AS
    SELECT * FROM read_parquet('{DATA_DIR / "dim_date.parquet"}')
""")

con.execute(f"""
    CREATE OR REPLACE TABLE dim_member AS
    SELECT * FROM read_parquet('{DATA_DIR / "dim_member.parquet"}')
""")

con.execute(f"""
    CREATE OR REPLACE TABLE dim_provider AS
    SELECT * FROM read_parquet('{DATA_DIR / "dim_provider.parquet"}')
""")

# Load fact table
con.execute(f"""
    CREATE OR REPLACE TABLE fact_claims AS
    SELECT * FROM read_parquet('{DATA_DIR / "fact_claims.parquet"}')
""")

con.close()

print("✅ DuckDB warehouse created successfully!")
print(f"📦 Database location: {DB_PATH}")
