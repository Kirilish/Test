# Car Assistant Telegram Bot (MVP++)

## Фичи
- Мульти-гараж: несколько авто, активная машина, переключение
- Тарифы: FREE (1 авто), PRO 99⭐ (до 3 авто)
- Лимиты ИИ: FREE 20/мес, PRO 200/мес
- VIN декодинг (NHTSA)
- История обслуживания: `/add_service`, `/history`
- Учет расходов: `/stats`
- OBD ошибки: `/error P0420` (+ ИИ объяснение)
- Напоминания: `/reminders`, `/notify_due`
- Чеклисты: `/checklist trip|winter`
- Подбор запчастей: `/parts`
- Админка: `/admin` (пользователи, PRO, монетизация, аналитика)

## Запуск
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
PYTHONPATH=src python -m bot.main
```
