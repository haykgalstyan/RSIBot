import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        RotatingFileHandler(
            "../../bot.log", maxBytes=10 * 1024 * 1024, backupCount=10
        ),
        logging.StreamHandler(),  # still see stuff in console/ssh
    ],
)

import asyncio
import ccxt.async_support as ccxt

from rsibot.alert import send_alert
from rsibot.config import (
    DATA_LENGTH,
    RSI_LENGTH,
    DATA_TIMEFRAME,
    SYMBOLS,
    RSI_OVERSOLD,
    RSI_OVERBOUGHT,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    DATA_POLL_INTERVAL_SECONDS,
)
from rsibot.data import fetch_data
from rsibot.indicators import (
    prepare_data,
    calculate_rsi,
    latest_rsi,
    is_interesting_rsi,
)

logger = logging.getLogger(__name__)

binance: ccxt.Exchange = ccxt.binance({"enableRateLimit": True})


async def fetch_rsi_for_symbol(symbol) -> float | None:
    data = await fetch_data(
        exchange=binance,
        symbol=symbol,
        timeframe=DATA_TIMEFRAME,
        limit=DATA_LENGTH,
    )
    if data is None:
        logger.error(f"No data found for {symbol}")
        return None

    rsi = (
        data.pipe(prepare_data)
        .pipe(
            calculate_rsi,
            rsi_length=RSI_LENGTH,
        )
        .pipe(latest_rsi)
    )
    return rsi


async def start_polling():
    while True:
        try:
            for symbol in SYMBOLS:
                rsi = await fetch_rsi_for_symbol(symbol)
                logger.info(f"{symbol} RSI: {rsi}")
                if is_interesting_rsi(rsi):
                    await alert(rsi, symbol)
        except Exception as e:
            logger.exception(e)

        await asyncio.sleep(DATA_POLL_INTERVAL_SECONDS)


async def alert(rsi: float | None, symbol: str):
    message = f"{symbol} RSI is {rsi:.1f} — {'OVERSOLD' if rsi <= RSI_OVERSOLD else 'OVERBOUGHT'}!"
    await send_alert(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message)
    logger.info(f"Alert sent for {symbol}")


async def main():
    try:
        await binance.load_markets()
        logger.info("Started")
        await start_polling()
    finally:
        await binance.close()


asyncio.run(main())
