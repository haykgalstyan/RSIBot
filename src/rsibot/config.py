from pathlib import Path
from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = ROOT_DIR / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        frozen=True,
        populate_by_name=True,
        alias_generator=lambda s: s.upper(),
        extra="ignore",
    )

    # Market data & indicators
    symbols: list[str] = Field(
        default_factory=lambda: ["BTC/USDT", "ETH/USDT", "SOL/USDT"]
    )
    data_poll_interval_seconds: int = Field(default=10, ge=5)
    data_timeframe: str = Field(default="15m")
    data_length: int = Field(default=120)
    rsi_length: int = Field(default=14, ge=7)

    # Alert thresholds
    rsi_overbought: float = Field(default=70.0)
    rsi_oversold: float = Field(default=30.0)

    # Telegram config
    telegram_bot_token: str = Field(default=...)
    telegram_chat_id: int = Field(default=...)

    @field_validator("symbols", mode="before")
    @classmethod
    def parse_symbols(cls, v: Any) -> list[str]:
        if isinstance(v, str):
            return [s.strip() for s in v.split(",") if s.strip()]
        return v
