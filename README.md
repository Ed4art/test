# tg-recipe-bot

A minimal Telegram bot that generates cooking recipes from provided ingredients using an LLM.

## Setup

1. Copy `.env.example` to `.env` and fill in the tokens.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the bot:
   ```bash
   make run
   ```

## Development

- `make format` – format the code with Black
- `make lint` – lint the code with Ruff
