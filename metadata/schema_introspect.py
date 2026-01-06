import duckdb
import yaml
import json
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "warehouse" / "warehouse.duckdb"
DOCS_PATH = Path(__file__).parent / "dbt_like_docs" / "models.yml"
OUTPUT_PATH = Path(__file__).parent / "metadata.json"

# Load YAML docs
with open(DOCS_PATH, "r") as f:
    docs = yaml.safe_load(f)

# Connect to DuckDB
con = duckdb.connect(DB_PATH)

catalog = []

for model in docs["models"]:
    table_name = model["name"]

    # Get schema from DuckDB
    schema_df = con.execute(
        f"PRAGMA table_info('{table_name}')"
    ).df()

    columns = []
    for _, row in schema_df.iterrows():
        col_doc = next(
            (c for c in model["columns"] if c["name"] == row["name"]),
            None
        )

        columns.append({
            "name": row["name"],
            "type": row["type"],
            "description": col_doc["description"] if col_doc else "",
            "pii": col_doc["pii"] if col_doc else False
        })

    catalog.append({
        "table": table_name,
        "description": model["description"],
        "grain": model["grain"],
        "pii": model["pii"],
        "columns": columns
    })

con.close()

# Write metadata catalog
with open(OUTPUT_PATH, "w") as f:
    json.dump(catalog, f, indent=2)

print("✅ Metadata catalog created successfully!")
print(f"📄 Output file: {OUTPUT_PATH}")
