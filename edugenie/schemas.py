from typing import List, Literal, Optional

from pydantic import BaseModel, Field, field_validator


class TextRequest(BaseModel):

    text: str = Field(
        ...,
        min_length=1,
        max_length=20000,
    )

    @field_validator("text")
    @classmethod
    def validate_text(cls, value):

        value = value.strip()

        if not value:

            raise ValueError(
                "Text cannot be empty."
            )

        return value


class QARequest(TextRequest):
    pass


class ExplainRequest(TextRequest):
    pass


class QuizRequest(TextRequest):
    pass


class SummaryRequest(TextRequest):
    pass


class LearningPathRequest(BaseModel):

    topic: str = Field(
        ...,
        min_length=1,
        max_length=500,
    )

    level: Literal[
        "beginner",
        "intermediate",
        "advanced",
    ] = "beginner"

    weekly_hours: int = Field(
        default=5,
        ge=1,
        le=40,
    )

    @field_validator("topic")
    @classmethod
    def validate_topic(cls, value):

        value = value.strip()

        if not value:

            raise ValueError(
                "Topic cannot be empty."
            )

        return value


class TextResponse(BaseModel):

    result: str


class QuizQuestion(BaseModel):

    question: str

    options: List[str] = Field(
        min_length=4,
        max_length=4,
    )

    correct_answer: str


class QuizResponse(BaseModel):

    questions: List[QuizQuestion] = Field(
        min_length=3,
        max_length=3,
    )


class LearningResource(BaseModel):

    title: str

    type: str

    url: Optional[str] = None

    why: str


class LearningStep(BaseModel):

    stage: Literal[
        "Beginner",
        "Intermediate",
        "Advanced",
    ]

    topics: List[str]

    estimated_weeks: int = Field(
        ge=1,
        le=52,
    )

    resources: List[
        LearningResource
    ] = Field(
        default_factory=list
    )


class LearningPathResponse(BaseModel):

    topic: str

    level: str

    weekly_hours: int

    steps: List[LearningStep]