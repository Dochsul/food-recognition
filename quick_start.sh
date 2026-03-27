#!/bin/bash

echo "🤖 Telegram Бот - Быстрый запуск"
echo "================================"
echo ""

# Проверка PyTorch
echo "Проверка зависимостей..."
python3 -c "import torch" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ PyTorch установлен"
else
    echo "❌ PyTorch не установлен"
    echo ""
    echo "Установите PyTorch:"
    echo "  pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu"
    echo ""
    exit 1
fi

# Проверка токена
if [ ! -f .env ]; then
    echo "❌ Файл .env не найден"
    exit 1
fi

source .env
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "❌ TELEGRAM_BOT_TOKEN не установлен в .env"
    exit 1
fi

echo "✅ Конфигурация OK"
echo ""
echo "🚀 Запускаю бота..."
echo "Для остановки нажмите Ctrl+C"
echo ""

python3 telegram_bot.py
