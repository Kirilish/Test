from __future__ import annotations

import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from bot.ai_service import AIService
from bot.config import settings
from bot.storage import JsonStorage
from bot.vin_service import VinService

logging.basicConfig(level=logging.INFO)

storage = JsonStorage()
vin_service = VinService()
ai_service = AIService(settings.hf_api_token, settings.hf_model)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Привет! Я авто-бот. Команды:\n"
        "/add_car <VIN> — добавить авто по VIN\n"
        "/my_car — показать авто\n"
        "/ask <вопрос> — спросить ИИ"
    )


async def add_car(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Укажите VIN: /add_car WDB12345678901234")
        return

    vin = context.args[0].strip().upper()
    await update.message.reply_text("Расшифровываю VIN...")
    try:
        data = await vin_service.decode(vin)
    except Exception as exc:
        await update.message.reply_text(f"Ошибка расшифровки VIN: {exc}")
        return

    storage.save_car(update.effective_user.id, data)
    await update.message.reply_text(_format_car(data))


async def my_car(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    car = storage.get_car(update.effective_user.id)
    if not car:
        await update.message.reply_text("Автомобиль не найден. Добавьте через /add_car <VIN>")
        return
    await update.message.reply_text(_format_car(car))


async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    question = " ".join(context.args).strip()
    if not question:
        await update.message.reply_text("Задайте вопрос: /ask Когда менять масло?")
        return

    car = storage.get_car(update.effective_user.id)
    answer = await ai_service.ask(question, car)
    await update.message.reply_text(answer[:4000])


async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Не понял сообщение. Используйте /start")


def _format_car(car: dict) -> str:
    return (
        "Ваш автомобиль:\n"
        f"VIN: {car.get('VIN')}\n"
        f"Марка: {car.get('Make')}\n"
        f"Модель: {car.get('Model')}\n"
        f"Год: {car.get('ModelYear')}\n"
        f"Кузов: {car.get('BodyClass')}\n"
        f"Двигатель: {car.get('Engine')}\n"
        f"Топливо: {car.get('FuelType')}\n"
        f"Привод: {car.get('DriveType')}\n"
        f"Страна сборки: {car.get('PlantCountry')}"
    )


def run() -> None:
    app = ApplicationBuilder().token(settings.telegram_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add_car", add_car))
    app.add_handler(CommandHandler("my_car", my_car))
    app.add_handler(CommandHandler("ask", ask))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fallback))
    app.run_polling()


if __name__ == "__main__":
    run()
