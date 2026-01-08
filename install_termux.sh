#!/bin/bash

# Простой скрипт установки бота в Termux (Android)

echo "📱 Установка Telegram бота в Termux"
echo "===================================="
echo ""

# Проверка что мы в Termux
if [ ! -d "/data/data/com.termux" ]; then
    echo "⚠️  Этот скрипт предназначен для Termux!"
    echo "Установите Termux из F-Droid: https://f-droid.org/en/packages/com.termux/"
    exit 1
fi

echo "1️⃣ Обновление пакетов..."
pkg update -y
pkg upgrade -y

echo ""
echo "2️⃣ Установка Python..."
pkg install python -y

echo ""
echo "3️⃣ Установка библиотеки Telegram..."
pip install python-telegram-bot

echo ""
echo "4️⃣ Создание файла бота..."
cat > ~/telegram_bot_simple.py << 'EOF'
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '🍔 Привет! Я бот для подсчета калорий!\n\n'
        '📸 Отправьте фото еды!\n'
        '/start - Начать\n'
        '/help - Помощь'
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'ℹ️ Это простая версия бота.\n'
        'Отправьте фото еды для тестирования!'
    )

async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f'📸 Фото получено!\n'
        f'Размер: {update.message.photo[-1].width}x{update.message.photo[-1].height}\n\n'
        f'✅ Бот работает правильно!'
    )

async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f'Получил сообщение: {update.message.text[:50]}\n\n'
        f'📸 Отправьте фото!'
    )

print("🤖 Запуск бота...")
app = Application.builder().token("8208188455:AAGa25OfMqTvM2bfhVIQkvwht2xvG8oDEmI").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(MessageHandler(filters.PHOTO, photo))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text))

print("✅ Бот запущен и работает!")
print("📱 Найдите бота: @my_calorietracker_bot")
print("🛑 Остановка: Ctrl+C")
print("")

try:
    app.run_polling()
except KeyboardInterrupt:
    print("\n👋 Бот остановлен")
EOF

echo ""
echo "✅ Установка завершена!"
echo ""
echo "📱 Для запуска бота введите:"
echo "   python ~/telegram_bot_simple.py"
echo ""
echo "🔋 Для работы в фоне:"
echo "   1. Установите: pkg install tmux"
echo "   2. Запустите: tmux"
echo "   3. Запустите бота: python ~/telegram_bot_simple.py"
echo "   4. Отключитесь: Ctrl+B затем D"
echo "   5. Вернуться: tmux attach"
echo ""
echo "Готово! 🚀"
