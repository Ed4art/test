import os
from pathlib import Path
from openai import OpenAI


def _load_prompt(name: str) -> str:
    path = Path("prompts") / name
    return path.read_text(encoding="utf-8")


SYSTEM_PROMPT = _load_prompt("recipe_system.md")
USER_TEMPLATE = _load_prompt("recipe_user_template.md")

_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def generate_recipe(ingredients: str) -> str:
    prompt = USER_TEMPLATE.format(ingredients=ingredients)
    response = _client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content.strip()
