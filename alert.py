from aiogram import Bot


async def send_alert(
    token: str,
    chat_id: int | str,
    text: str,
) -> None:
    bot = Bot(token=token)
    try:
        await bot.send_message(chat_id=chat_id, text=text)
    finally:
        await bot.session.close()
