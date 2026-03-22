# RSIBot

Simple async RSI watcher for Binance that pings you on Telegram when RSI goes overbought/oversold.

## Setup
1. `uv sync`
2. Copy `.env.example` to `.env` and fill in your `TELEGRAM_TOKEN` + `CHAT_ID`
3. `uv run python main.py`
