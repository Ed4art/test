# Команды управления проектом
.PHONY: run lint format

run:
	# Запуск бота
	python bot.py

lint:
	# Проверка стиля кода
	ruff check .

format:
	# Форматирование кода
	black .
