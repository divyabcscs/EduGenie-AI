from config import get_settings

from gemini_client import get_gemini_service
from local_explainer import get_local_explainer


SYSTEM_PROMPT = """
You are EduGenie.

Explain academic concepts to beginners.

Use:

1. Simple definition
2. Easy analogy
3. Practical example
4. Common misconception

Keep the explanation clear and educational.
"""


def explain_concept(topic: str) -> str:

    settings = get_settings()

    backend = (
        settings.explanation_backend
        .lower()
    )

    if backend in {
        "auto",
        "local",
    }:

        try:

            explainer = get_local_explainer()

            return explainer.explain(
                topic
            )

        except Exception:

            if backend == "local":

                raise

    prompt = f"""
Explain the following concept
for a beginner.

Concept:
{topic}

Include:

- Definition
- Analogy
- Example
- Common misconception
"""

    service = get_gemini_service()

    return service.generate_text(
        prompt,
        system_instruction=SYSTEM_PROMPT,
    )