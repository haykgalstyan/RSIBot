import logging

import asyncio
import ccxt.async_support as ccxt

from rsibot.config import Settings
from rsibot.logger import configure_logger
from rsibot.data import fetch_data
from rsibot.indicators import (
    prepare_data,
    calculate_rsi,
    latest_rsi,
)
from rsibot.bot import RSIBot

configure_logger()
logger = logging.getLogger(__name__)


async def fetch_rsi_for_symbol(
    exchange: ccxt.Exchange,
    symbol: str,
    settings: Settings,
) -> float | None:
    data = await fetch_data(
        exchange=exchange,
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


async def start_polling(bot: RSIBot):
    while True:
        try:
            results = await asyncio.gather(
                *[
                    fetch_rsi_for_symbol(bot.exchange, symbol, bot.settings)
                    for symbol in bot.settings.symbols
                ],
                return_exceptions=True,
            )

            for symbol, result in zip(bot.settings.symbols, results):
                if isinstance(result, Exception):
                    logger.error(f"{symbol} failed: {result}")
                    continue

                rsi = result
                logger.info(f"{symbol} RSI: {rsi}")

                if rsi is None:
                    continue

                if (
                    rsi <= bot.settings.rsi_oversold
                    or rsi >= bot.settings.rsi_overbought
                ):
                    await alert(rsi, symbol, bot)

        except Exception as e:
            logger.exception(e)

        await asyncio.sleep(bot.settings.data_poll_interval_seconds)


async def alert(rsi: float, symbol: str, bot: RSIBot):
    direction = "OVERSOLD" if rsi <= bot.settings.rsi_oversold else "OVERBOUGHT"
    message = f"{symbol} RSI: {rsi:.1f} {direction}!"

    await bot.send_alert(message)
    logger.info(f"Alert sent for {symbol}")


async def main() -> None:
    settings = Settings()
    async with RSIBot(settings) as bot:
        logger.info("RSIBot started successfully. Markets loaded.")
        await start_polling(bot)


try:
    asyncio.run(main())
except (KeyboardInterrupt, SystemExit):
    logger.info("Stopped Gracefully")
except Exception as e:
    logger.exception("Unexpected death")
