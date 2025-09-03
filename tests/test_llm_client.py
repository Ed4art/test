"""Тесты для клиента генерации рецептов."""

import json
import pytest

import llm_client
from llm_client import RecipeLLM, RecipeLLMError


class DummyClient:
    """Заглушка клиента DeepSeek."""

    def __init__(self, responses: list[str]) -> None:
        self.responses = responses
        self.index = 0

    def chat_completion(self, *args, **kwargs):
        content = self.responses[self.index]
        self.index += 1
        return content


def test_generate_valid_json(monkeypatch) -> None:
    """Успешная генерация рецепта при корректном JSON."""
    response = json.dumps(
        {
            "name": "Суп",
            "ingredients": ["вода"],
            "steps": ["Налить воду"],
            "nutrition": {
                "calories": 1,
                "protein": 0.1,
                "fat": 0.0,
                "carbs": 0.2,
            },
            "cholesterol_mg": 0,
            "glycemic_index": 5,
        }
    )
    monkeypatch.setattr(llm_client, "_client", DummyClient([response]))
    recipe = RecipeLLM.generate("вода", "simple")
    assert recipe.name == "Суп"


def test_generate_invalid_json(monkeypatch) -> None:
    """Ошибка при двух некорректных ответах модели."""
    monkeypatch.setattr(llm_client, "_client", DummyClient(["bad", "still bad"]))
    with pytest.raises(RecipeLLMError):
        RecipeLLM.generate("вода", "simple")
