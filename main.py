import asyncio
from aiogram import Bot, Dispatcher
import openai

# Настройки
TELEGRAM_TOKEN = "ТВОЙ_ТОКЕН_БОТА"
OPENAI_API_KEY = "ТВОЙ_OPENAI_API_KEY"
CHAT_ID = "ТВОЙ_ЧАТ_ID"  # Куда бот будет слать сообщения

bot = Bot(token=TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY

async def ask_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

async def scheduled_task():
    while True:
        # Запрос к нейросети
        answer = await ask_gpt("Напиши что-нибудь интересное о технологиях.")
        
        # Отправка в Telegram
        await bot.send_message(
            chat_id=CHAT_ID,
            text=f"🔮 Ответ нейросети:\n\n{answer}\n\n"
                 f"📎 Ссылка на диалог: https://chat.openai.com (пример, реальную ссылку нужно генерировать)"
        )
        
        # Ждём, например, 1 час (3600 секунд)
        await asyncio.sleep(3600)

async def main():
    asyncio.create_task(scheduled_task())
    dp = Dispatcher(bot)
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
