import os
from dotenv import load_dotenv

load_dotenv()


# Market data and indicators
DATA_TIMEFRAME: str = os.getenv("DATA_TIMEFRAME", "15m")  # candle size
DATA_POLL_INTERVAL_SECONDS: int = 10
RSI_LENGTH: int = int(os.getenv("RSI_LENGTH", "14"))
DATA_LENGTH: int = RSI_LENGTH * 2
SYMBOLS: list[str] = os.getenv("SYMBOLS", "BTC/USDT,ETH/USDT").split(",")

# Alert thresholds
RSI_OVERBOUGHT: float = 70.0
RSI_OVERSOLD: float = 30.0

# Alerts Config
TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise ValueError(
        "TELEGRAM_BOT_TOKEN is missing! Add it to .env or set as environment variable."
    )

TELEGRAM_CHAT_ID: int = int(os.getenv("TELEGRAM_CHAT_ID"))
if TELEGRAM_CHAT_ID == 0:
    raise ValueError(
        "TELEGRAM_CHAT_ID is missing! Add it to .env or set as environment variable."
    )
