from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from aiogram import types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove


# Убираем кнопки под вводом
# @dp.message(Command("done"))
# async def cmd_done(message: types.Message):
#     await message.answer(
#         "Клавиатура скрыта.",
#         reply_markup=ReplyKeyboardRemove(),
#     )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [["Кнопка 1", "Кнопка 3"]]
    markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text("Выберите:", reply_markup=markup)


async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"Вы нажали: {text}")


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Убираем клавиатуру
    await update.message.reply_text(
        "Завершаем работу. Клавиатура скрыта.",
        reply_markup=ReplyKeyboardRemove(),
    )

# Настройка и запуск бот
app = Application.builder().token("7219188035:AAF7gXFGGyAnNwqtzOej7bmUdoDyL-1a9NA").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle_buttons))
# app.add_handler(CommandHandler("done", done))
app.run_polling()