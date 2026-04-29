# Car Assistant Telegram Bot (MVP)

Telegram-бот для автовладельцев:
- Добавление автомобиля по VIN (`/add_car`)
- Хранение данных автомобиля
- Вопросы к ИИ (`/ask`)

## Стек
- Python 3.11+
- python-telegram-bot
- NHTSA VIN Decoder API
- Hugging Face Inference API

## Быстрый старт
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
```

Заполните `.env`:
- `TELEGRAM_BOT_TOKEN` — токен Telegram-бота
- `HF_API_TOKEN` — (опционально) токен Hugging Face

Запуск:
```bash
PYTHONPATH=src python -m bot.main
```

## Команды бота
- `/start`
- `/add_car <VIN>`
- `/my_car`
- `/ask <вопрос>`

## Примечания MVP
- Основной источник VIN-данных: NHTSA.
- Если `HF_API_TOKEN` пустой, используется fallback-ответ без внешнего ИИ.
