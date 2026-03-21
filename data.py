import logging

import ccxt.async_support as ccxt
import pandas as pd

logger = logging.getLogger(__name__)


async def fetch_data(
    exchange: ccxt.Exchange,
    symbol: str,
    timeframe: str,
    limit: int = 100,
) -> pd.DataFrame | None:
    await exchange.load_markets()

    try:
        data = await exchange.fetch_ohlcv(
            symbol=symbol,
            timeframe=timeframe,
            limit=limit,
        )
    except Exception as e:
        logger.error(f"Error fetching data {e}")
        return None

    df = pd.DataFrame(
        data,
        columns=[
            "timestamp",
            "open",
            "high",
            "low",
            "close",
            "volume",
        ],
    )
    return df
