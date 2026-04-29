# Car Assistant — Telegram Mini App

Архитектура: **Telegram Bot + Mini App (Web) + FastAPI backend + JSON DB (MVP)**.

## Что реализовано
- Bot как точка входа и уведомления (`/start`, `/plans`, `/upgrade_99`, `/notify_due`, `/admin`)
- Mini App интерфейс (`src/webapp/index.html`):
  - Главный экран
  - Гараж (список авто, активная машина)
  - Добавление авто по VIN
  - История
  - Напоминания
  - Расходы
- Backend API (`src/backend/app.py`):
  - `/api/garage`, `/api/car/add_by_vin`, `/api/car/switch/{idx}`
  - `/api/service/add`, `/api/history`, `/api/reminders`, `/api/stats`, `/api/admin`
- Тарифы FREE/PRO 99⭐ и лимиты машин/ИИ
- Админ-аналитика: пользователи, PRO, выручка, популярные машины/вопросы

## Запуск
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
```

### Backend API
```bash
PYTHONPATH=src uvicorn backend.app:app --reload --port 8000
```

### Bot
```bash
PYTHONPATH=src python -m bot.main
```

Разместите `src/webapp/index.html` на HTTPS-домене и укажите `MINI_APP_URL` в `.env`.
