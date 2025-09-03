"""Тесты для функции format_markdown."""

from llm_client import Nutrition, Recipe
from formatters import format_markdown


def test_format_markdown_basic() -> None:
    """Проверяет корректность Markdown-формата."""
    recipe = Recipe(
        name="Омлет",
        ingredients=["яйцо", "молоко"],
        steps=["Смешать", "Жарить"],
        nutrition=Nutrition(calories=100, protein=10, fat=5, carbs=1),
        cholesterol_mg=200,
        glycemic_index=50,
    )

    result = format_markdown(recipe)

    assert "*Омлет*" in result
    assert "- яйцо" in result
    assert "1. Смешать" in result
    assert "| 100 | 10.0 | 5.0 | 1.0 |" in result
    assert "Холестерин: 200 мг" in result
