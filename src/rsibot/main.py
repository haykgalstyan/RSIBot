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


from rsibot.config import Settings
from rsibot.alert import send_alert
from rsibot.data import fetch_data
from rsibot.indicators import (
    prepare_data,
    calculate_rsi,
    latest_rsi,
)

logger = logging.getLogger(__name__)

binance: ccxt.Exchange = ccxt.binance({"enableRateLimit": True})


async def fetch_rsi_for_symbol(
    symbol: str,
    settings: Settings,
) -> float | None:
    data = await fetch_data(
        exchange=binance,
        symbol=symbol,
        timeframe=settings.data_timeframe,
        limit=settings.data_length,
    )
    if data is None:
        logger.error(f"No data found for {symbol}")
        return None

    rsi = (
        data.pipe(prepare_data)
        .pipe(
            calculate_rsi,
            rsi_length=settings.rsi_length,
        )
        .pipe(latest_rsi)
    )
    return rsi


async def start_polling(
    settings: Settings,
):
    while True:
        try:
            for symbol in settings.symbols:
                rsi = await fetch_rsi_for_symbol(symbol, settings)
                logger.info(f"{symbol} RSI: {rsi}")
                if (
                    rsi <= settings.rsi_oversold
                    or rsi >= settings.rsi_overbought
                ):
                    await alert(rsi, symbol, settings)
        except Exception as e:
            logger.exception(e)

        await asyncio.sleep(settings.data_poll_interval_seconds)


async def alert(
    rsi: float | None,
    symbol: str,
    settings: Settings,
):
    message = f"{symbol} RSI is {rsi:.1f} — {'OVERSOLD' if rsi <= settings.rsi_oversold else 'OVERBOUGHT'}!"
    await send_alert(
        token=settings.telegram_bot_token,
        chat_id=settings.telegram_chat_id,
        text=message,
    )
    logger.info(f"Alert sent for {symbol}")


async def main():
    try:
        settings = Settings()
        await binance.load_markets()
        logger.info("Started")
        await start_polling(settings)
    finally:
        await binance.close()


asyncio.run(main())
