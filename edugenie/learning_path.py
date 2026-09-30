from gemini_client import get_gemini_service
from schemas import LearningPathResponse


SYSTEM_PROMPT = """
You are EduGenie, an educational curriculum designer.

Create structured learning paths.

The path must progress through:

Beginner
Intermediate
Advanced

Include:

- Topics
- Estimated duration
- Useful learning resources

Do not invent resource URLs.
If you are not confident about a URL,
return null for the URL.
"""


def get_learning_recommendations(
    topic: str,
    level: str,
    weekly_hours: int,
) -> LearningPathResponse:

    prompt = f"""
Create a personalized learning path.

Topic:
{topic}

Current Level:
{level}

Available Study Time:
{weekly_hours} hours per week.

Create three stages:

1. Beginner
2. Intermediate
3. Advanced

For every stage include:

- Topics
- Estimated weeks
- Useful resources
- Why each resource is useful
"""

    service = get_gemini_service()

    return service.generate_structured(
        prompt,
        LearningPathResponse,
        system_instruction=SYSTEM_PROMPT,
    )