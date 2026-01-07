#!/bin/bash

# Скрипт для запуска Telegram бота подсчета калорий

echo "🤖 Telegram Бот для Подсчета Калорий"
echo "====================================="
echo ""

# Проверка наличия .env файла
if [ ! -f .env ]; then
    echo "⚠️  Файл .env не найден!"
    echo "📝 Создайте файл .env из примера:"
    echo "   cp .env.example .env"
    echo ""
    echo "🔑 Добавьте ваш Telegram Bot Token в файл .env"
    echo ""
    exit 1
fi

# Загрузка переменных окружения
export $(cat .env | grep -v '^#' | xargs)

# Проверка наличия токена
if [ -z "$TELEGRAM_BOT_TOKEN" ] || [ "$TELEGRAM_BOT_TOKEN" = "your_bot_token_here" ]; then
    echo "❌ TELEGRAM_BOT_TOKEN не установлен!"
    echo "📝 Откройте файл .env и установите правильный токен"
    echo ""
    exit 1
fi

# Проверка установки зависимостей
if ! python -c "import telegram" 2>/dev/null; then
    echo "📦 Устанавливаю зависимости..."
    pip install -r requirements.txt
    echo ""
fi

# Запуск бота
echo "🚀 Запускаю бота..."
echo "📱 Модель: ${MODEL_NAME:-yolov5s}"
echo ""

if [ -z "$MODEL_NAME" ]; then
    python telegram_bot.py
else
    python telegram_bot.py --model $MODEL_NAME
fi
