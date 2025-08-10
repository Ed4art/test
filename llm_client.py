"""Клиент LLM для генерации рецептов с валидированным JSON-ответом."""

from __future__ import annotations

import json
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from openai import DeepSeek
from pydantic import BaseModel, ValidationError

load_dotenv()  # загрузка переменных окружения из .env


def _load_prompt(name: str) -> str:
    """Читает текст подсказки из каталога prompts."""

    path = Path("prompts") / name
    return path.read_text(encoding="utf-8")


SYSTEM_PROMPT = _load_prompt("recipe_system.md")
USER_TEMPLATE = _load_prompt("recipe_user_template.md")


class Nutrition(BaseModel):
    """Пищевая ценность рецепта."""

    calories: int
    protein: float
    fat: float
    carbs: float


class Recipe(BaseModel):
    """Модель рецепта, которую возвращает LLM."""

    name: str
    ingredients: List[str]
    steps: List[str]
    nutrition: Nutrition
    cholesterol_mg: int
    glycemic_index: int
    approx: bool


class RecipeLLM:
    """Обёртка над DeepSeek для генерации рецептов."""

    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.7) -> None:
        self._client = DeepSeek()
        self._model = model
        self._temperature = temperature

        self._schema = {
            "type": "json_schema",
            "json_schema": {
                "name": "recipe",
                "schema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "ingredients": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "steps": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "nutrition": {
                            "type": "object",
                            "properties": {
                                "calories": {"type": "integer"},
                                "protein": {"type": "number"},
                                "fat": {"type": "number"},
                                "carbs": {"type": "number"},
                            },
                            "required": [
                                "calories",
                                "protein",
                                "fat",
                                "carbs",
                            ],
                        },
                        "cholesterol_mg": {"type": "integer"},
                        "glycemic_index": {"type": "integer"},
                        "approx": {"type": "boolean"},
                    },
                    "required": [
                        "name",
                        "ingredients",
                        "steps",
                        "nutrition",
                        "cholesterol_mg",
                        "glycemic_index",
                        "approx",
                    ],
                },
            },
        }

    def generate_recipe(self, ingredients: str) -> Recipe:
        """Формирует рецепт на основе списка ингредиентов."""

        prompt = USER_TEMPLATE.format(ingredients=ingredients)
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ]

        # Две попытки получения корректного JSON от модели
        for _ in range(2):
            try:
                response = self._client.chat.completions.create(
                    model=self._model,
                    messages=messages,
                    temperature=self._temperature,
                    response_format=self._schema,
                )
            except Exception:
                # Повторный запрос без structured outputs
                messages.append(
                    {
                        "role": "system",
                        "content": "Всегда отвечай строго в JSON по оговорённой схеме.",
                    }
                )
                response = self._client.chat.completions.create(
                    model=self._model,
                    messages=messages,
                    temperature=self._temperature,
                )

            content = response.choices[0].message["content"]
            try:
                data = json.loads(content)
                return Recipe.model_validate(data)
            except (json.JSONDecodeError, ValidationError):
                messages.append({"role": "assistant", "content": content})
                messages.append(
                    {
                        "role": "user",
                        "content": "Верни корректный JSON по согласованной схеме.",
                    }
                )

        raise ValueError("Модель не вернула корректный JSON")


__all__ = ["RecipeLLM", "Recipe", "Nutrition"]
