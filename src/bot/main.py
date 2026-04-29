from __future__ import annotations

from telegram import KeyboardButton, ReplyKeyboardMarkup, Update, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from bot.config import settings
from bot.storage import JsonStorage

storage = JsonStorage()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    kb = ReplyKeyboardMarkup(
        [[KeyboardButton(text="Открыть гараж", web_app=WebAppInfo(url=settings.mini_app_url))]],
        resize_keyboard=True,
    )
    await update.message.reply_text(
        "Открой Mini App кнопкой ниже.\nБыстрые команды: /plans /upgrade_99 /notify_due /admin",
        reply_markup=kb,
    )


async def plans(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("FREE: 1 авто\nPRO 99⭐: до 3 авто + расширенный ИИ")


async def upgrade_99(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    storage.upgrade_to_pro(update.effective_user.id)
    await update.message.reply_text("✅ PRO активирован (MVP-эмуляция оплаты Stars)")


async def notify_due(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    car = storage.get_active_car(update.effective_user.id)
    if not car:
        await update.message.reply_text("Добавьте авто через Mini App")
        return
    mileage = int(car.get("mileage", 0))
    await update.message.reply_text(f"🔔 Пора планировать ТО: масло до {mileage+9000} км")


async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    uid = update.effective_user.id
    admins = {int(x) for x in settings.admin_ids.split(",") if x.strip()}
    if admins and uid not in admins:
        await update.message.reply_text("Нет доступа")
        return
    a = storage.analytics()
    await update.message.reply_text(
        f"Users:{a['users']} PRO:{a['pro_users']} Revenue⭐:{a['revenue_stars']}\n"
        f"Popular cars:{a['popular_cars']}\nPopular questions:{a['popular_questions']}"
    )


def run() -> None:
    app = ApplicationBuilder().token(settings.telegram_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("plans", plans))
    app.add_handler(CommandHandler("upgrade_99", upgrade_99))
    app.add_handler(CommandHandler("notify_due", notify_due))
    app.add_handler(CommandHandler("admin", admin))
    app.run_polling()


if __name__ == "__main__":
    run()
