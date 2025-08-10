"""Обёртка для обращения к LLM и генерации рецептов."""

import os
from pathlib import Path
from deepseek import DeepSeekAPI


def _load_prompt(name: str) -> str:
    """Читает текст подсказки из каталога prompts."""
    path = Path("prompts") / name
    return path.read_text(encoding="utf-8")


SYSTEM_PROMPT = _load_prompt("recipe_system.md")
USER_TEMPLATE = _load_prompt("recipe_user_template.md")

_client = DeepSeekAPI(
    api_key=os.environ.get("DEEPSEEK_API_KEY")
)  # инициализация клиента


def generate_recipe(ingredients: str) -> str:
    """Формирует рецепт на основе списка ингредиентов."""
    prompt = USER_TEMPLATE.format(ingredients=ingredients)
    response = _client.chat_completion(
        prompt,
        prompt_sys=SYSTEM_PROMPT,
        model="deepseek-chat",
    )
    return response.strip()
