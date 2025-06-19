import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import ReplyKeyboardRemove

TOKEN = "7219188035:AAF7gXFGGyAnNwqtzOej7bmUdoDyL-1a9NA"
MY_TG_ID = 1287372767  # ID должен быть int, а не str

bot = Bot(token=TOKEN)
dp = Dispatcher()
active_chats = {MY_TG_ID}


async def send_message(text: str):
    try:
        await bot.send_message(chat_id=MY_TG_ID, text=text)
    except Exception as e:
        print(f"Ошибка отправки: {e}")


async def cleanup():
    """Убираем клавиатуры во всех активных чатах"""
    for chat_id in list(active_chats):
        try:
            await bot.send_message(
                chat_id=chat_id,
                text="Бот завершает работу",
                reply_markup=ReplyKeyboardRemove()
            )
        except Exception as e:
            print(f"Ошибка в чате {chat_id}: {str(e)}")
        finally:
            active_chats.discard(chat_id)


async def shutdown():
    """Корректное завершение работы"""
    await send_message("Простите, сплю...")
    await cleanup()
    await bot.session.close()


async def main():
    # Отправляем сообщение о старте
    await send_message("Проснулась :)")

    # Создаем Task для поллинга
    polling_task = asyncio.create_task(dp.start_polling(bot))

    # Ожидаем завершения (которого не будет, пока бот работает)
    try:
        await polling_task
    except asyncio.CancelledError:
        pass
    finally:
        await shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass