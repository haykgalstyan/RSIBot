import pandas as pd
import pandas_ta as ta


def prepare_data(
    data: pd.DataFrame,
) -> pd.DataFrame:
    return data.assign(
        date_time=pd.to_datetime(data["timestamp"], unit="ms"),
    )


def calculate_rsi(
    data: pd.DataFrame,
    rsi_length: int = 14,
) -> pd.DataFrame:
    return data.assign(
        rsi=ta.rsi(data["close"], length=rsi_length),
    )


def latest_rsi(
    data: pd.DataFrame,
) -> float | None:
    return data.tail(1)["rsi"].item()
