import asyncio
import ccxt.async_support as ccxt
from config import DATA_LENGTH, RSI_LENGTH, FETCH_TIMEFRAME, SYMBOLS
from data import fetch_data
from indicators import prepare_data, calculate_rsi, latest_rsi
import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        RotatingFileHandler(
            "bot.log", maxBytes=10 * 1024 * 1024, backupCount=10
        ),
        logging.StreamHandler(),  # still see stuff in console/ssh
    ],
)

logger = logging.getLogger(__name__)

binance: ccxt.Exchange = ccxt.binance({"enableRateLimit": True})


async def fetch_rsi_for_symbol(symbol) -> float | None:
    data = await fetch_data(
        exchange=binance,
        symbol=symbol,
        timeframe=FETCH_TIMEFRAME,
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


async def main():
    try:
        await binance.load_markets()
        for symbol in SYMBOLS:
            rsi = await fetch_rsi_for_symbol(symbol)
            logger.info(f"{symbol} RSI: {rsi}")

    finally:
        await binance.close()


asyncio.run(main())
