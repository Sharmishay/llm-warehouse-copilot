from llm.llm_helper import enhance_question
from metadata.search_catalog import search_catalog, load_catalog
from metadata.query_planner import plan_query
from metadata.sql_generator import generate_sql
from metadata.sql_executor import execute_sql
from metadata.visualizer import visualize
import duckdb


def run_pipeline(user_question):
    print(f"\n❓ Question: {user_question}")

    # 1. Load catalog
    catalog = load_catalog()

    # 2. Search relevant tables
    search_results = search_catalog(user_question, catalog)
    if not search_results:
        print("❌ No relevant tables found.")
        return

    print("\n🔍 Relevant tables:")
    for r in search_results:
        print(f"- {r['table']} (score={r['score']})")

    # 3. Plan query
    query_plan = plan_query(user_question, catalog, search_results)
    print("\n🧠 Query Plan:")
    print(query_plan)

    # 4. Generate SQL
    sql = generate_sql(query_plan)
    print("\n🧾 Generated SQL:")
    print(sql)

    # 5. Execute SQL
    df = execute_sql(sql)
    print("\n📊 Query Result:")
    print(df.head())

    # 6. Visualize
    visualize(df)


if __name__ == "__main__":
    raw_question = input("\n💬 Ask a data question: ")
    question = enhance_question(raw_question)
    print(f"\n🧠 Interpreted question: {question}")

    run_pipeline(question)
