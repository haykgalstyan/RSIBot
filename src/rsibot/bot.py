from aiogram import Bot
import ccxt.async_support as ccxt
from .config import Settings
import logging

logger = logging.getLogger(__name__)


class RSIBot:

    def __init__(self, settings: Settings):
        self.settings = settings
        self.exchange: ccxt.Exchange = ccxt.binance({"enableRateLimit": True})
        self.telegram: Bot = Bot(token=settings.telegram_bot_token)

    async def __aenter__(self):
        await self.exchange.load_markets()
        logger.info("RSIBot: Ready")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.exchange.close()
        await self.telegram.session.close()
        logger.info("RSIBot: Disposed")

    async def send_alert(self, message: str) -> None:
        await self.telegram.send_message(
            chat_id=self.settings.telegram_chat_id,
            text=message,
            parse_mode="HTML",
        )
