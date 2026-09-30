from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import get_settings
from explanation_module import explain_concept
from learning_path import get_learning_recommendations
from qna import answer_question
from quiz_module import generate_quiz
from schemas import (
    ExplainRequest,
    LearningPathRequest,
    LearningPathResponse,
    QARequest,
    QuizRequest,
    QuizResponse,
    SummaryRequest,
    TextResponse,
)
from summary_module import summarize_text


settings = get_settings()

BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="EduGenie - Google Gemini Powered Learning Assistant",
)


app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)


templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "app_name": settings.app_name
        },
    )


@app.get("/health")
async def health():

    return {
        "status": "ok",
        "application": settings.app_name,
        "version": settings.app_version,
        "gemini_configured": bool(settings.gemini_api_key),
        "explanation_backend": settings.explanation_backend,
    }


@app.post("/qa", response_model=TextResponse)
async def qa(request: QARequest):

    try:

        result = answer_question(request.text)

        return TextResponse(
            result=result
        )

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        )


@app.post("/explain", response_model=TextResponse)
async def explain(request: ExplainRequest):

    try:

        result = explain_concept(request.text)

        return TextResponse(
            result=result
        )

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        )


@app.post("/quiz", response_model=QuizResponse)
async def quiz(request: QuizRequest):

    try:

        return generate_quiz(
            request.text
        )

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        )


@app.post("/summarize", response_model=TextResponse)
async def summarize(request: SummaryRequest):

    try:

        result = summarize_text(
            request.text
        )

        return TextResponse(
            result=result
        )

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        )


@app.post(
    "/learn/recommendations",
    response_model=LearningPathResponse,
)
async def learning_path(request: LearningPathRequest):

    try:

        return get_learning_recommendations(
            topic=request.topic,
            level=request.level,
            weekly_hours=request.weekly_hours,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        )