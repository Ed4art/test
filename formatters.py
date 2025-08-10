"""Форматирование рецептов для отправки пользователю."""

from telegram.helpers import escape_markdown

from llm_client import Recipe


def format_recipe(recipe: Recipe) -> str:
    """Превращает объект рецепта в Markdown-строку."""

    lines: list[str] = []

    lines.append(f"*{escape_markdown(recipe.name, version=1)}*")
    lines.append("")
    lines.append("*Ингредиенты:*")
    for item in recipe.ingredients:
        lines.append(f"- {escape_markdown(item, version=1)}")

    lines.append("")
    lines.append("*Шаги:*")
    for idx, step in enumerate(recipe.steps, 1):
        lines.append(f"{idx}. {escape_markdown(step, version=1)}")

    lines.append("")
    lines.append("*КБЖУ:*")
    lines.append("| Ккал | Белки г | Жиры г | Углеводы г |")
    lines.append("| --- | --- | --- | --- |")
    n = recipe.nutrition
    lines.append(f"| {n.calories} | {n.protein} | {n.fat} | {n.carbs} |")

    lines.append(f"Холестерин: {recipe.cholesterol_mg} мг; ГИ: {recipe.glycemic_index}")
    if recipe.approx:
        lines.append("_значения приблизительные_")

    return "\n".join(lines)


__all__ = ["format_recipe"]
