# RSIBot

RSI watcher bot for Binance that pings you on Telegram when crypto goes
overbought/oversold.

## Install

### Docker

```bash
cp .env.example .env
docker compose up -d --build
```

### Update

```bash
git pull && docker compose up -d --build
```

### Local

```bash
uv sync
cp .env.example .env
uv run python -m rsibot.main
```

### Configuration

Edit `.env`:

```
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id
SYMBOLS=BTC/USDT,ETH/USDT,SOL/USDT
Optional: RSI_OVERBOUGHT, RSI_OVERSOLD, DATA_TIMEFRAME
```
