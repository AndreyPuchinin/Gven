import signal
import asyncio
from telegram import Bot
from telegram.error import TelegramError

TOKEN = "7219188035:AAF7gXFGGyAnNwqtzOej7bmUdoDyL-1a9NA"  # Замени на токен бота
CHAT_ID = "1287372767"  # Узнать через @userinfobot


bot = Bot(token=TOKEN)


async def send_message(text):
    try:
        await bot.send_message(chat_id=CHAT_ID, text=text)
    except TelegramError as e:
        print(f"Ошибка отправки: {e}")


async def main():
    # Отправляем сообщение о старте
    await send_message("Проснулась :)")

    # Создаем событие для ожидания
    stop_event = asyncio.Event()

    # Обработчик сигналов
    def signal_handler(signum, frame):
        # Запускаем отправку сообщения в существующем event loop
        asyncio.create_task(shutdown())

    async def shutdown():
        await send_message("Простите, сплю...")
        stop_event.set()

    # Регистрируем обработчики сигналов
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Ждем сигнала остановки
    await stop_event.wait()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass  # Обработка Ctrl+C уже сделана в signal_handler