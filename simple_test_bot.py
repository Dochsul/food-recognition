#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Простой тестовый Telegram бот - БЕЗ моделей распознавания
Для проверки что токен работает и бот может подключиться к Telegram
"""

import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    await update.message.reply_text(
        "🍔 Привет! Я тестовый бот для подсчета калорий.\n\n"
        "✅ Я работаю!\n"
        "📸 Отправьте мне фото, и я скажу что получил его.\n\n"
        "Команды:\n"
        "/start - Это сообщение\n"
        "/help - Помощь\n"
        "/status - Статус бота"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    await update.message.reply_text(
        "ℹ️ Это простая тестовая версия бота.\n\n"
        "Основная функция (распознавание еды) требует:\n"
        "• PyTorch и модели YOLO (~1GB)\n"
        "• Доступ к интернету для Telegram API\n\n"
        "Сейчас бот просто отвечает на сообщения,\n"
        "чтобы проверить что токен работает правильно."
    )


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /status"""
    await update.message.reply_text(
        "✅ Бот работает!\n"
        "📡 Подключение к Telegram API: OK\n"
        "🔑 Токен: Действителен\n\n"
        "Готов к работе!"
    )


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик фотографий"""
    await update.message.reply_text(
        "📸 Фото получено!\n\n"
        "ℹ️ Это тестовая версия бота.\n"
        "Для распознавания еды нужно запустить полную версию с моделями.\n\n"
        "Размер фото: {} x {} пикселей".format(
            update.message.photo[-1].width,
            update.message.photo[-1].height
        )
    )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений"""
    await update.message.reply_text(
        "📝 Получил ваше сообщение: '{}'\n\n"
        "📸 Отправьте мне фото еды для тестирования!\n"
        "Используйте /help для помощи.".format(update.message.text[:50])
    )


def main():
    """Запуск бота"""
    # Получаем токен
    token = os.getenv('TELEGRAM_BOT_TOKEN')

    if not token:
        import sys
        if len(sys.argv) > 2 and sys.argv[1] == '--token':
            token = sys.argv[2]
        else:
            print("❌ ОШИБКА: Токен не найден!")
            print("Используйте:")
            print("  export TELEGRAM_BOT_TOKEN=ваш_токен")
            print("  python simple_test_bot.py")
            print("ИЛИ:")
            print("  python simple_test_bot.py --token ваш_токен")
            return

    print(f"🤖 Запуск тестового бота...")
    print(f"🔑 Токен: {token[:10]}...{token[-5:]}")
    print(f"📡 Подключение к Telegram API...")

    # Создаем приложение
    application = Application.builder().token(token).build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # Запускаем бота
    print("✅ Бот запущен и работает!")
    print("📱 Найдите бота в Telegram: @my_calorietracker_bot")
    print("🛑 Для остановки нажмите Ctrl+C")
    print()

    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен")


if __name__ == '__main__':
    main()
