# Car Assistant Telegram Bot (MVP+)

Telegram-бот для автовладельцев с бесплатным функционалом и тарифами.

## Что умеет
- Добавление авто по VIN: `/add_car <VIN>`
- Список машин и переключение активной: `/list_cars`, `/switch_car <номер>`
- Показ активной машины: `/my_car`
- ИИ-ответы по машине: `/ask <вопрос>`
- Рекомендации по обслуживанию: `/service`
- Подсказки по ошибкам OBD-II: `/error P0420`
- Помощь с подбором запчастей: `/parts <деталь>`
- Тарифы: `/plans`

## Тарифы (MVP)
- **FREE (0⭐)**: 1 машина, базовые ответы.
- **PRO (99⭐)**: 2 машины, более подробные рекомендации.

> Для MVP PRO активируется командой `/upgrade_99`.

## Стек
- Python 3.11+
- python-telegram-bot
- NHTSA VIN Decoder API (бесплатно)
- Hugging Face Inference API (опционально, с бесплатным лимитом)

## Быстрый старт
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
PYTHONPATH=src python -m bot.main
```

## ENV
- `TELEGRAM_BOT_TOKEN` — токен Telegram-бота
- `HF_API_TOKEN` — токен HF (опционально)
- `HF_MODEL` — модель HF
