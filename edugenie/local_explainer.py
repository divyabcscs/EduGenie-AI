from functools import lru_cache

from config import get_settings


class LocalExplainer:

    def __init__(self):

        self.settings = get_settings()

        self.tokenizer = None

        self.model = None

    def load_model(self):

        try:

            from transformers import (
                AutoModelForSeq2SeqLM,
                AutoTokenizer,
            )

        except ImportError as exc:

            raise RuntimeError(
                "Local AI dependencies are not installed. "
                "Run: pip install -r requirements-local.txt"
            ) from exc

        model_id = (
            self.settings.local_model_id
        )

        cache_dir = (
            self.settings.model_cache_dir
        )

        self.tokenizer = (
            AutoTokenizer.from_pretrained(
                model_id,
                cache_dir=cache_dir,
            )
        )

        self.model = (
            AutoModelForSeq2SeqLM.from_pretrained(
                model_id,
                cache_dir=cache_dir,
            )
        )

    def explain(self, topic: str) -> str:

        if self.model is None:

            self.load_model()

        prompt = f"""
Explain this concept to a beginner.

Use simple language.

Give a short analogy
and one practical example.

Concept:
{topic[:self.settings.local_max_input_chars]}
"""

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=1024,
        )

        outputs = self.model.generate(

            **inputs,

            max_new_tokens=(
                self.settings.local_max_new_tokens
            ),

            num_beams=4,

            early_stopping=True,
        )

        return self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True,
        ).strip()


@lru_cache
def get_local_explainer():

    return LocalExplainer()