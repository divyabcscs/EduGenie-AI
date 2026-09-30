import json
import time
from typing import Type

from google import genai
from google.genai import types

from config import get_settings


class GeminiService:
    def __init__(self):
        settings = get_settings()

        if not settings.gemini_api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured. "
                "Please add it to your .env file."
            )

        self.settings = settings
        self.client = genai.Client(
            api_key=settings.gemini_api_key
        )

    def _generate(self, prompt, config):
        last_error = None

        for attempt in range(4):
            try:
                return self.client.models.generate_content(
                    model=self.settings.gemini_model,
                    contents=prompt,
                    config=config,
                )

            except Exception as exc:
                last_error = exc

                if "503" not in str(exc):
                    raise

                wait_time = 2 ** attempt
                time.sleep(wait_time)

        raise last_error

    def generate_text(
        self,
        prompt: str,
        system_instruction: str | None = None,
    ) -> str:

        config = types.GenerateContentConfig(
            temperature=self.settings.gemini_temperature,
            max_output_tokens=self.settings.gemini_max_output_tokens,
            system_instruction=system_instruction,
        )

        response = self._generate(prompt, config)

        text = getattr(response, "text", None)

        if not text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return text.strip()

    def generate_structured(
        self,
        prompt: str,
        response_schema: Type,
        system_instruction: str | None = None,
    ):

        config = types.GenerateContentConfig(
            temperature=self.settings.gemini_temperature,
            max_output_tokens=self.settings.gemini_max_output_tokens,
            response_mime_type="application/json",
            response_schema=response_schema,
            system_instruction=system_instruction,
        )

        response = self._generate(prompt, config)

        text = getattr(response, "text", None)

        if not text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        try:
            return response_schema.model_validate_json(text)

        except Exception:
            cleaned = text.strip()

            if cleaned.startswith("```"):
                cleaned = cleaned.split("\n", 1)[1]
                cleaned = cleaned.rsplit("```", 1)[0].strip()

            try:
                return response_schema.model_validate(
                    json.loads(cleaned)
                )

            except Exception as exc:
                raise RuntimeError(
                    "Gemini returned invalid JSON."
                ) from exc


def get_gemini_service():
    return GeminiService()