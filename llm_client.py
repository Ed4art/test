"""Обёртка для обращения к LLM и генерации рецептов."""

from pathlib import Path
from typing import List

from dotenv import load_dotenv
from openai import OpenAI
from openai.error import OpenAIError, RateLimitError
from pydantic import BaseModel, ValidationError


load_dotenv()  # загрузка переменных окружения из .env


def _load_prompt(name: str) -> str:
    """Читает текст подсказки из каталога prompts."""
    path = Path("prompts") / name
    return path.read_text(encoding="utf-8")


SYSTEM_PROMPT = _load_prompt("recipe_system.md")
USER_TEMPLATE = _load_prompt("recipe_user_template.md")

_client = OpenAI()  # инициализация клиента с API-ключом из окружения


class Nutrition(BaseModel):
    """Модель данных для блока КБЖУ."""

    calories: int
    protein: float
    fat: float
    carbs: float


class Recipe(BaseModel):
    """Модель итогового рецепта."""

    name: str
    ingredients: List[str]
    steps: List[str]
    nutrition: Nutrition
    cholesterol_mg: int
    glycemic_index: int
    approx: bool | None = None


class RecipeLLMError(Exception):
    """Базовая ошибка генерации рецепта."""


class RecipeLLM:
    """Клиент генерации рецептов через LLM."""

    @staticmethod
    def generate(ingredients: str, mood: str) -> Recipe:
        """Вызывает модель и возвращает валидированный рецепт."""

        prompt = USER_TEMPLATE.replace("{{ingredients_csv}}", ingredients).replace(
            "{{mood}}", mood
        )

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ]

        for attempt in range(2):
            try:
                response = _client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                )
            except (RateLimitError, OpenAIError) as exc:
                raise RecipeLLMError("Сервис недоступен, попробуйте позже") from exc

            content = response.choices[0].message.content.strip()

            try:
                return Recipe.model_validate_json(content)
            except ValidationError:
                if attempt == 0:
                    messages.append({"role": "assistant", "content": content})
                    messages.append(
                        {
                            "role": "user",
                            "content": "Ответ не в формате JSON. "
                            "Верни только корректный JSON по схеме.",
                        }
                    )
                    continue
                raise RecipeLLMError("Модель вернула некорректный ответ")

        raise RecipeLLMError("Модель вернула некорректный ответ")


__all__ = ["RecipeLLM", "Recipe", "RecipeLLMError"]
