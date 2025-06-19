# ОГЛАВЛЕНИЕ:
# ==========
# ЛИБЫ
# ПЕРЕМЕННЫЕ
# РАБОТА С БД
# ОБЩИЕ ФУНКЦИИ
# РАБОТА С КНОПКАМИ
# КОМАНДЫ
# ОБРАБОТКА ВВОДА
# РАБОТА С СЕРВЕРОМ
# ЗАПУСК! 17А.

# ===== ЛИБЫ =====
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from telegram.error import TelegramError
import asyncio
import json
from pathlib import Path
from aiogram.types import ReplyKeyboardRemove
from Loggers import JsonFileLogger, ProjLogger, TimeEntryLogger
from TodayDataTime import get_current_time_in_formats, final_regex
# ===== КОНЕЦ ЛИБ =====

# ===== ПЕРЕМЕННЫЕ =====
JSON_FILE = "projects.json"
dp = Dispatcher()
user_data = {}  # Временное хранилище для ввода данных
# КОМАНДЫ
add_proj = "Добавить проект"
add_task = "Добавить подзадачу"
show_all_collection = "Показать всю коллекцию"
Json_file_logger = JsonFileLogger("Json_file_logger")
TOKEN = "7219188035:AAF7gXFGGyAnNwqtzOej7bmUdoDyL-1a9NA"  # Замени на токен бота
My_tg_id = 1287372767  # Узнать через @userinfobot
active_chats = {My_tg_id}
bot = Bot(token=TOKEN)
# ===== КОНЕЦ ПЕРЕМЕННЫХ =====


# ===== РАБОТА С БД =====
def load_data():
    if not Path(JSON_FILE).exists():
        return {"projects": []}
    with open(JSON_FILE, "r", encoding="utf-8") as fr:
        try:
            Json_file_logger.FormatIsCorrect()
            return json.load(fr)
        except json.decoder.JSONDecodeError:
            Json_file_logger.FormatError()
            return {"projects": []}


def save_data(data):
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
# ===== КОНЕЦ РАБОТЫ С БД =====


# ===== ОБЩИЕ ФУНКЦИИ =====
async def ask_for_name(user_id: int, action: str):
    await bot.send_message(user_id, "Введите имя:")
    print(user_data, user_id)
    if user_id not in user_data:
        user_data[user_id] = {"action": action, "step": "name"}
    else:
        await bot.send_message(user_id, "Проект с таким названием уже есть!")


async def ask_for_description(user_id: int):
    await bot.send_message(user_id, "Введите описание:")
    user_data[user_id]["step"] = "description"


async def ask_for_time(user_id: int):
    await bot.send_message(
        user_id,
        f"⏰ Введите время (формат: <code>год.месяц.день часы:минуты</code>)\n"
        f"Например, <code>{get_current_time_in_formats()['full_format']}</code>\n"
        f"или: <code>{get_current_time_in_formats()['short_format']}</code>",
        parse_mode="HTML"
    )
    user_data[user_id]["step"] = "time"
# ===== КОНЕЦ ОБЩИХ ФУНКЦИЙ =====


# ===== РАБОТА С КНОПКАМИ =====
async def cleanup():
    """Убираем клавиатуры во всех активных чатах"""
    for chat_id in list(active_chats):
        try:
            await bot.send_message(
                chat_id=chat_id,
                text="Простите, сплю...",
                reply_markup=ReplyKeyboardRemove()
            )
        except Exception as e:
            print(f"Ошибка в чате {chat_id}: {str(e)}")
        finally:
            active_chats.discard(chat_id)
# ===== КОНЕЦ # РАБОТЫ С КНОПКАМИ =====


# ===== КОМАНДЫ =====
@dp.message(Command("add_project"))
async def add_project_cmd(message: types.Message):
    load_data()
    if not Json_file_logger.get_correctness():
        for one_error in Json_file_logger._errors:
            await message.answer(one_error)
        return
    await ask_for_name(message.from_user.id, "add_project")


@dp.message(Command("add_task"))
async def add_task_cmd(message: types.Message):
    data = load_data()
    proj_logger = ProjLogger("proj_logger")
    if not data or not data["projects"]:
        proj_logger.NoProject()
    if not Json_file_logger.get_correctness() or not proj_logger.get_correctness():
        for one_error in Json_file_logger._errors:
            await message.answer(one_error)
        for one_error in proj_logger._errors:
            await message.answer(one_error)
        return
    await ask_for_name(message.from_user.id, "add_task")


@dp.message(Command("show_data"))
async def show_data_cmd(message: types.Message):
    data = load_data()
    await message.answer(f"<pre>{json.dumps(data, indent=2)}</pre>", parse_mode="HTML")
# ===== КОНЕЦ КОМАНД =====


# ===== ОБРАБОТКА ВВОДА =====
@dp.message(F.text)
async def handle_input(message: types.Message):
    """Обработка обычных сообщений"""
    user_id = message.from_user.id

    if user_id not in user_data:
        await message.answer("Простите, не понимаю...")
        return

    current_data = user_data[user_id]
    text = message.text.strip()
    time_entry_logger = TimeEntryLogger("time_entry_logger")

    if current_data["step"] == "name":
        user_data[user_id]["name"] = text
        await ask_for_description(user_id)

    elif current_data["step"] == "description":
        user_data[user_id]["description"] = text
        await ask_for_time(user_id)

    elif current_data["step"] == "time":
        if not bool(final_regex.fullmatch(text)):
            time_entry_logger.EntryFormatError()
            for one_error in time_entry_logger._errors:
                await message.answer(one_error)
            return

        user_data[user_id]["time"] = text
        action = current_data["action"]
        data = load_data()

        if action == "add_project":
            new_project = {
                "name": current_data["name"],
                "status": "x",
                "description": current_data["description"],
                "time": current_data["time"],
                "tasks": []
            }

            data["projects"].append(new_project)
            await message.answer(f"✅ Проект <b>{current_data['name']}</b> создан!", parse_mode="HTML")

        elif action == "add_task":
            # Добавляем задачу в последний проект (или последнюю задачу)
            if data["projects"]:
                target = data["projects"][-1]  # По умолчанию в последний проект
                # Если есть вложенные задачи, ищем последнюю
                while "tasks" in target and target["tasks"]:
                    target = target["tasks"][-1]

                new_task = {
                    "name": current_data["name"],
                    "status": "x",
                    "description": current_data["description"],
                    "time": current_data["time"],
                    "tasks": []
                }

                target["tasks"].append(new_task)
                await message.answer(f"✅ Задача <b>{current_data['name']}</b> добавлена!", parse_mode="HTML")

        save_data(data)
        del user_data[user_id]
# ===== КОНЕЦ ОБРАБОТКИ ВВОДА =====


# ===== РАБОТА С СЕРВЕРОМ =====
async def send_message(text):
    try:
        await bot.send_message(chat_id=My_tg_id, text=text)
    except TelegramError as e:
        print(f"Ошибка отправки: {e}")


async def shutdown():
    """Корректное завершение работы"""
    await cleanup()
    await bot.session.close()


async def main():
    # Отправляем сообщение о старте
    await cleanup()
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
# ===== КОНЕЦ РАБОТЫ С СЕРВЕРОМ =====


# ЗАПУСК! 17A.
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass  # Обработка Ctrl+C уже сделана в signal_handler