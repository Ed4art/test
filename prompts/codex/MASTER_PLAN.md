Ты — ассистент-разработчик. Сгенерируй MVP Telegram-бота «AI Recipe Bot» (Python).
Цели:
- Подбор рецепта по ингредиентам и настроению (simple/fancy).
- Возврат КБЖУ (ккал, белки г, жиры г, углеводы г), холестерина (мг) и приблизительного гликемического индекса (GI).
- Всё зашито в один репозиторий, без внешних кулинарных API. Питсведения возвращает LLM как оценку.

Требования к стеку:
- python-telegram-bot ≥ 21, long polling.
- Официальный DeepSeek Python SDK; использовать Chat Completions или Responses API (Completions legacy не применять).
- В идеале Structured Outputs/JSON Schema; если недоступно — валидировать JSON pydantic’ом.

Сборка репозитория (в этом порядке):
1) scaffold: структура, `.gitignore`, `requirements.txt`, `.env.example`, `README.md`.
2) `prompts/runtime/recipe_system.md`, `prompts/runtime/recipe_user_template.md`.
3) код: `llm_client.py`, `formatters.py`, `bot.py`.
4) простой smoke-test и инструкции запуска.

Соблюдай шаги и приемлемую краткость кода/README. Все секреты — только через `.env`.
