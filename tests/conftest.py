"""Общие настройки тестов."""

import os
import sys
from pathlib import Path

# Подставляем API-ключ для клиента DeepSeek
os.environ.setdefault("DEEPSEEK_API_KEY", "test")

# Добавляем корень репозитория в sys.path для импорта модулей
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
