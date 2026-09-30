from gemini_client import get_gemini_service


SYSTEM_PROMPT = """
You are EduGenie, an educational summarizer.

Summarize educational content clearly.

Preserve:

- Important facts
- Key concepts
- Relationships

Remove:

- Repetition
- Unnecessary wording

Do not add information
that is not present in the source.
"""


def summarize_text(text: str) -> str:

    prompt = f"""
Summarize the following educational passage.

Provide:

1. Short overview
2. Important points
3. Key facts

Passage:

{text}
"""

    service = get_gemini_service()

    return service.generate_text(
        prompt,
        system_instruction=SYSTEM_PROMPT,
    )