# RSIBot

RSI watcher bot for Binance that pings you on Telegram when RSI goes overbought/oversold.

## Setup

1. `uv sync`
2. `cp .env.example .env` and fill in your `TELEGRAM_TOKEN` + `CHAT_ID`
3. `uv run python -m rsibot.main`