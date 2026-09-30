from gemini_client import get_gemini_service
from schemas import QuizResponse


SYSTEM_PROMPT = """
You are an educational quiz generator.

Create exactly three multiple-choice questions.

Each question must contain:

- One question
- Exactly four options
- One correct answer

The correct answer must exactly match
one of the four options.

Questions must be based only
on the supplied educational content.
"""


def generate_quiz(
    passage: str
) -> QuizResponse:

    prompt = f"""
Create a 3-question MCQ quiz
from the following passage.

Requirements:

- 3 questions
- 4 options per question
- Plausible distractors
- Exactly one correct answer
- Correct answer must match an option exactly

Passage:

{passage}
"""

    service = get_gemini_service()

    return service.generate_structured(
        prompt,
        QuizResponse,
        system_instruction=SYSTEM_PROMPT,
    )