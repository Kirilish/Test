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
        "🚗 Авто-бот готов.\n"
        "Бесплатно: 1 машина + базовые советы.\n"
        "PRO (99 Stars): 2 машины + расширенные подсказки.\n\n"
        "Команды:\n"
        "/add_car <VIN>\n/list_cars\n/switch_car <номер>\n/my_car\n"
        "/ask <вопрос>\n/error <код>\n/service\n/parts <деталь>\n"
        "/plans\n/upgrade_99"
    )


async def plans(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Тарифы:\n"
        "FREE — 0⭐: 1 авто, базовая VIN информация, базовые ответы ИИ.\n"
        "PRO — 99⭐: 2 авто, расширенные диагностические рекомендации, расширенный разбор вопросов.\n"
        "Для MVP: активируйте PRO командой /upgrade_99"
    )


async def upgrade_99(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    storage.upgrade_to_pro(update.effective_user.id)
    await update.message.reply_text("✅ Тариф PRO (99⭐) активирован. Теперь можно добавить вторую машину.")


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

    ok, msg = storage.add_car(update.effective_user.id, data)
    if not ok:
        await update.message.reply_text(f"❌ {msg}. Перейдите на /plans")
        return

    await update.message.reply_text("Машина добавлена как активная.\n" + _format_car(data))


async def list_cars(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    cars = storage.list_cars(update.effective_user.id)
    if not cars:
        await update.message.reply_text("Нет добавленных машин")
        return
    lines = [f"{i+1}. {c.get('Make')} {c.get('Model')} ({c.get('ModelYear')})" for i, c in enumerate(cars)]
    await update.message.reply_text("Ваши машины:\n" + "\n".join(lines))


async def switch_car(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("Использование: /switch_car <номер>")
        return
    idx = int(context.args[0]) - 1
    if not storage.set_active_car(update.effective_user.id, idx):
        await update.message.reply_text("Неверный номер машины")
        return
    car = storage.get_active_car(update.effective_user.id)
    await update.message.reply_text("Активная машина обновлена:\n" + _format_car(car or {}))


async def my_car(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    car = storage.get_active_car(update.effective_user.id)
    if not car:
        await update.message.reply_text("Автомобиль не найден. Добавьте через /add_car <VIN>")
        return
    await update.message.reply_text(_format_car(car))


async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    question = " ".join(context.args).strip()
    if not question:
        await update.message.reply_text("Задайте вопрос: /ask Когда менять масло?")
        return

    profile = storage.get_profile(update.effective_user.id)
    car = storage.get_active_car(update.effective_user.id)
    answer = await ai_service.ask(question, car, profile.get("plan", "free"))
    await update.message.reply_text(answer[:4000])


async def service(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    car = storage.get_active_car(update.effective_user.id)
    if not car:
        await update.message.reply_text("Сначала добавьте авто: /add_car <VIN>")
        return
    await update.message.reply_text(
        f"ТО для {car.get('Make')} {car.get('Model')}:\n"
        "• Масло/фильтр: каждые 8-10 тыс. км\n"
        "• Тормозная жидкость: раз в 2 года\n"
        "• Свечи/фильтры: по регламенту производителя"
    )


async def error_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Укажите код, например: /error P0420")
        return
    code = context.args[0].upper()
    hints = {
        "P0420": "Низкая эффективность катализатора. Проверьте лямбда-зонд и утечки.",
        "P0300": "Случайные пропуски зажигания. Проверьте свечи, катушки, топливо.",
        "P0171": "Слишком бедная смесь. Проверьте подсос воздуха и MAF.",
    }
    await update.message.reply_text(hints.get(code, "Код не найден в базе MVP. Рекомендуется диагностика OBD-II."))


async def parts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    part = " ".join(context.args).strip() or "расходники"
    car = storage.get_active_car(update.effective_user.id)
    if not car:
        await update.message.reply_text("Сначала добавьте авто: /add_car <VIN>")
        return
    await update.message.reply_text(
        f"Подбор '{part}' для {car.get('Make')} {car.get('Model')}:\n"
        "1) Сверьте VIN и год выпуска\n"
        "2) Сравните OEM номер из каталога производителя\n"
        "3) Проверьте совместимость по двигателю/кузову"
    )


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
    app.add_handler(CommandHandler("plans", plans))
    app.add_handler(CommandHandler("upgrade_99", upgrade_99))
    app.add_handler(CommandHandler("add_car", add_car))
    app.add_handler(CommandHandler("list_cars", list_cars))
    app.add_handler(CommandHandler("switch_car", switch_car))
    app.add_handler(CommandHandler("my_car", my_car))
    app.add_handler(CommandHandler("ask", ask))
    app.add_handler(CommandHandler("service", service))
    app.add_handler(CommandHandler("error", error_help))
    app.add_handler(CommandHandler("parts", parts))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fallback))
    app.run_polling()


if __name__ == "__main__":
    run()
