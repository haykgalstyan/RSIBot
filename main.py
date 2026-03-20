from typing import Optional

import asyncio
import ccxt.async_support as ccxt
import pandas as pd
import pandas_ta as ta

binance: ccxt.Exchange = ccxt.binance({"enableRateLimit": True})
fetch_timeframe = "15m"


async def fetch_crypto_data(
    exchange: ccxt.Exchange,
    symbol: str,
    timeframe: str,
    limit: int = 100,
) -> Optional[pd.DataFrame]:
    async with exchange:
        await exchange.load_markets()

        print(f"Fetching data for {symbol}")
        try:
            data = await exchange.fetch_ohlcv(
                symbol=symbol,
                timeframe=timeframe,
                limit=limit,
            )
        except Exception as e:
            print(f"Error fetching data {e}")
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


async def calculate_rsi(
    df: pd.DataFrame,
    rsa_length: int = 14,
) -> pd.Series:
    df["ts"] = pd.to_datetime(df["timestamp"], unit="ms")
    rsi = ta.rsi(df["close"], length=rsa_length)
    return rsi


async def main():
    data = await fetch_crypto_data(binance, "ETH/USDT", fetch_timeframe)
    if data is not None:
        rsi_data = await calculate_rsi(data)
        print(rsi_data.tail(10))

asyncio.run(main())
