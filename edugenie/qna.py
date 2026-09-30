from gemini_client import get_gemini_service


SYSTEM_PROMPT = """
You are EduGenie, an educational AI assistant.

Answer student questions accurately and clearly.

Rules:

1. Start with the direct answer.
2. Explain the answer in simple language.
3. Add an example when useful.
4. Avoid unnecessary jargon.
5. Do not invent facts.
6. If information is uncertain, say so.
"""


def answer_question(question: str) -> str:

    prompt = f"""
Answer the following learner question.

Question:
{question}

Provide a concise educational response.
"""

    service = get_gemini_service()

    return service.generate_text(
        prompt,
        system_instruction=SYSTEM_PROMPT,
    )