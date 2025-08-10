"""Обёртка для обращения к LLM и генерации рецептов."""

from pathlib import Path

from dotenv import load_dotenv
from deepseek import DeepSeekAPI

load_dotenv()  # загрузка переменных окружения из .env


def _load_prompt(name: str) -> str:
    """Читает текст подсказки из каталога prompts."""
    path = Path("prompts") / name
    return path.read_text(encoding="utf-8")


SYSTEM_PROMPT = _load_prompt("recipe_system.md")
USER_TEMPLATE = _load_prompt("recipe_user_template.md")

_client = DeepSeekAPI()  # инициализация клиента с API-ключом из окружения


def generate_recipe(ingredients: str) -> str:
    """Формирует рецепт на основе списка ингредиентов."""
    prompt = USER_TEMPLATE.format(ingredients=ingredients)
    response = _client.chat_completion(
        prompt=prompt,
        prompt_sys=SYSTEM_PROMPT,
    )
    return response.strip()
