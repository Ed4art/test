"""Обёртка для обращения к LLM и генерации рецептов."""

from pathlib import Path

from dotenv import load_dotenv
from deepseek import DeepSeekAPI
from pydantic import BaseModel, ConfigDict, ValidationError


load_dotenv()  # загрузка переменных окружения из .env


def _load_prompt(name: str) -> str:
    """Читает текст подсказки из каталога prompts."""
    path = Path("prompts") / name
    return path.read_text(encoding="utf-8")


SYSTEM_PROMPT = _load_prompt("recipe_system.md")
USER_TEMPLATE = _load_prompt("recipe_user_template.md")

_client = DeepSeekAPI()  # инициализация клиента с API-ключом из окружения


class Nutrition(BaseModel):
    """Модель данных для блока КБЖУ."""

    calories: int
    protein: float
    fat: float
    carbs: float

    model_config = ConfigDict(extra="forbid")


class Recipe(BaseModel):
    """Модель итогового рецепта."""

    name: str
    ingredients: list[str]
    steps: list[str]
    nutrition: Nutrition
    cholesterol_mg: int
    glycemic_index: int
    approx: bool | None = None

    model_config = ConfigDict(extra="forbid")


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

        messages: list[dict[str, str]] = []

        for attempt in range(2):
            try:
                if attempt == 0:
                    content = _client.chat_completion(
                        prompt=prompt, prompt_sys=SYSTEM_PROMPT
                    )
                else:
                    content = _client.chat_completion(prompt=messages)
            except Exception as exc:  # noqa: BLE001
                raise RecipeLLMError("Сервис недоступен, попробуйте позже") from exc

            try:
                return Recipe.model_validate_json(content.strip())
            except ValidationError:
                if attempt == 0:
                    messages = [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": prompt},
                        {"role": "assistant", "content": content},
                        {
                            "role": "user",
                            "content": (
                                "Ответ не в формате JSON. "
                                "Верни только корректный JSON по схеме."
                            ),
                        },
                    ]
                    continue
                raise RecipeLLMError("Модель вернула некорректный ответ")

        raise RecipeLLMError("Модель вернула некорректный ответ")


__all__ = ["RecipeLLM", "Recipe", "RecipeLLMError"]
