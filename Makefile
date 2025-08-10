.PHONY: run lint format

run:
	python bot.py

lint:
	ruff check .

format:
	black .
