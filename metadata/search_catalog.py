import json
from pathlib import Path

CATALOG_PATH = Path(__file__).parent / "metadata.json"


def load_catalog():
    with open(CATALOG_PATH, "r") as f:
        return json.load(f)


def search_catalog(query, catalog):
    words = query.lower().split()
    matches = []

    for table in catalog:
        score = 0

        # Search table description
        for word in words:
            if word in table["description"].lower():
                score += 2

        # Search column names & descriptions
        for col in table["columns"]:
            for word in words:
                if word in col["name"].lower():
                    score += 1
                if word in col["description"].lower():
                    score += 1

        if score > 0:
            matches.append({
                "table": table["table"],
                "score": score,
                "description": table["description"]
            })

    return sorted(matches, key=lambda x: x["score"], reverse=True)


if __name__ == "__main__":
    catalog = load_catalog()

    user_query = input("🔍 Enter your question: ")
    results = search_catalog(user_query, catalog)

    print("\n📊 Relevant tables:")
    for r in results:
        print(f"- {r['table']} (score={r['score']})")
        print(f"  {r['description']}")
