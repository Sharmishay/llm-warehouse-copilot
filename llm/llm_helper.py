import os

LLM_ENABLED = False
client = None

try:
    from openai import OpenAI

    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        client = OpenAI(api_key=api_key)
        LLM_ENABLED = True
except Exception:
    LLM_ENABLED = False


def enhance_question(user_question: str) -> str:
    """
    Enhances the user's question using an LLM.
    Falls back safely if no API key is configured.
    """

    if not LLM_ENABLED:
        return user_question  # ✅ graceful fallback

    prompt = f"""
You are a data analytics assistant.
Rewrite the user's question into a clear analytics question.

Rules:
- Do NOT write SQL
- Do NOT mention tables
- Keep it short

User question:
{user_question}

Normalized question:
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content.strip()
