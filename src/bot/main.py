from __future__ import annotations

import logging
from datetime import date

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
ADMIN_IDS = {int(x) for x in settings.admin_ids.split(",") if x.strip()} if hasattr(settings, "admin_ids") else set()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "🚗 MVP+ авто-бот\n"
        "FREE: 1 авто, до 20 ИИ-запросов/мес\n"
        "PRO 99⭐: до 3 авто, до 200 ИИ-запросов/мес\n"
        "Команды: /plans /add_car /list_cars /switch_car /my_car /ask /service /error /parts /add_service /history /stats /checklist /reminders /notify_due"
    )


async def plans(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("FREE: 1 авто, базовый ИИ\nPRO (99⭐): 3 авто, больше ИИ, глубже диагностика\nMVP upgrade: /upgrade_99")


async def upgrade_99(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    storage.upgrade_to_pro(update.effective_user.id)
    await update.message.reply_text("✅ PRO активирован за 99⭐ (MVP-эмуляция).")


async def add_car(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("/add_car <VIN>")
        return
    vin = context.args[0].strip().upper()
    data = await vin_service.decode(vin)
    ok, msg = storage.add_car(update.effective_user.id, data)
    if not ok:
        await update.message.reply_text(msg)
        return
    await update.message.reply_text("Добавлено:\n" + _format_car(data) + "\n\nНапоминания: /reminders")


async def list_cars(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    cars = storage.list_cars(update.effective_user.id)
    if not cars:
        await update.message.reply_text("Машин нет")
        return
    await update.message.reply_text("\n".join([f"{i+1}) {c.get('nickname')} [{c.get('VIN')}]" for i, c in enumerate(cars)]))


async def switch_car(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("/switch_car <номер>")
        return
    if storage.set_active_car(update.effective_user.id, int(context.args[0]) - 1):
        await update.message.reply_text("Активная машина переключена")
    else:
        await update.message.reply_text("Неверный индекс")


async def my_car(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    car = storage.get_active_car(update.effective_user.id)
    await update.message.reply_text(_format_car(car or {}))


async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    question = " ".join(context.args).strip()
    if not question:
        await update.message.reply_text("/ask <вопрос>")
        return
    allowed, msg = storage.can_use_ai(update.effective_user.id)
    if not allowed:
        await update.message.reply_text(msg)
        return
    profile = storage.get_profile(update.effective_user.id)
    car = storage.get_active_car(update.effective_user.id)
    history = storage.service_history(update.effective_user.id)[-5:]
    prompt_q = f"{question}\nПоследние обслуживания: {history}"
    answer = await ai_service.ask(prompt_q, car, profile.get("plan", "free"))
    storage.mark_ai_usage(update.effective_user.id, question)
    await update.message.reply_text(answer[:4000])


async def error_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    code = (context.args[0].upper() if context.args else "")
    mapping = {"P0420": "Катализатор/лямбда", "P0300": "Пропуски зажигания", "P0171": "Бедная смесь"}
    base = mapping.get(code, "Неизвестный код")
    profile = storage.get_profile(update.effective_user.id)
    car = storage.get_active_car(update.effective_user.id)
    ai = await ai_service.ask(f"Объясни OBD ошибку {code}: {base}", car, profile.get("plan", "free"))
    await update.message.reply_text(f"{code}: {base}\n{ai[:1500]}")


async def service(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("ТО: масло 8-10к, тормозная 2 года, ГРМ 60-100к")


async def add_service(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) < 4:
        await update.message.reply_text("/add_service <название> <пробег> <стоимость> <категория>")
        return
    title, mileage, cost, category = context.args[0], int(context.args[1]), float(context.args[2]), context.args[3]
    storage.add_service_record(update.effective_user.id, title, mileage, cost, category)
    await update.message.reply_text("✅ Запись ТО добавлена")


async def history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    items = storage.service_history(update.effective_user.id)
    if not items:
        await update.message.reply_text("История пустая")
        return
    text = "\n".join([f"{x['date']} | {x['title']} | {x['mileage']} км | {x['cost']}" for x in items[-20:]])
    await update.message.reply_text(text)


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    s = storage.expense_stats(update.effective_user.id)
    await update.message.reply_text(f"Расходы: {s['total']}\nОпераций: {s['count']}\nПо категориям: {s['by_category']}")


async def reminders(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    car = storage.get_active_car(update.effective_user.id)
    if not car:
        await update.message.reply_text("Добавьте авто")
        return
    mileage = int(car.get("mileage", 0))
    oil_due = mileage + 9000
    timing_due = mileage + 70000
    await update.message.reply_text(f"Напоминания:\n• Масло до {oil_due} км\n• ГРМ до {timing_due} км\n• Тормоза: проверка каждые 15 000 км")


async def notify_due(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await reminders(update, context)


async def checklist(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    mode = (context.args[0] if context.args else "trip").lower()
    if mode == "winter":
        text = "Перед зимой: АКБ, антифриз, зимняя резина, щетки, омывайка"
    else:
        text = "Перед поездкой: давление шин, масло, тормоза, документы, аптечка"
    await update.message.reply_text(text)


async def parts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    part = " ".join(context.args) or "расходники"
    car = storage.get_active_car(update.effective_user.id) or {}
    await update.message.reply_text(f"Подбор {part} для {car.get('Make')} {car.get('Model')}:\nOEM: ищите по VIN\nАналоги: Bosch/Mahle/Denso (проверить применимость)")


async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    uid = update.effective_user.id
    if ADMIN_IDS and uid not in ADMIN_IDS:
        await update.message.reply_text("Нет доступа")
        return
    a = storage.analytics()
    await update.message.reply_text(f"Users: {a['users']}\nPRO: {a['pro_users']}\nRevenue⭐: {a['revenue_stars']}\nCars: {a['popular_cars']}\nQuestions: {a['popular_questions']}")


async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text("Не понял. /start")


def _format_car(car: dict) -> str:
    return f"VIN:{car.get('VIN')}\n{car.get('Make')} {car.get('Model')} {car.get('ModelYear')}\nПробег:{car.get('mileage', 0)}"


def run() -> None:
    app = ApplicationBuilder().token(settings.telegram_token).build()
    for cmd, handler in [
        ("start", start), ("plans", plans), ("upgrade_99", upgrade_99), ("add_car", add_car),
        ("list_cars", list_cars), ("switch_car", switch_car), ("my_car", my_car), ("ask", ask),
        ("service", service), ("add_service", add_service), ("history", history), ("error", error_help),
        ("parts", parts), ("stats", stats), ("checklist", checklist), ("reminders", reminders),
        ("notify_due", notify_due), ("admin", admin),
    ]:
        app.add_handler(CommandHandler(cmd, handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fallback))
    app.run_polling()


if __name__ == "__main__":
    run()
