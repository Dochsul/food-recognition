#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Тест работы Telegram бота - проверка подключения
"""

import os
import sys

def test_bot_token():
    """Проверка токена и подключения к Telegram API"""

    print("🔍 Тестирование подключения к Telegram...\n")

    # Загружаем .env
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except:
        pass

    token = os.getenv('TELEGRAM_BOT_TOKEN')

    if not token:
        print("❌ TELEGRAM_BOT_TOKEN не найден в .env")
        return False

    print(f"✓ Токен найден: {token[:10]}...{token[-5:]}")
    print(f"✓ Длина токена: {len(token)}")
    print()

    # Проверяем подключение к Telegram API
    try:
        import telegram
        import asyncio

        print("Проверяем подключение к Telegram API...")

        async def check_bot():
            bot = telegram.Bot(token=token)
            me = await bot.get_me()
            return me

        # Запускаем проверку
        me = asyncio.run(check_bot())

        print(f"\n✅ БОТ РАБОТАЕТ!")
        print(f"   • Username: @{me.username}")
        print(f"   • Имя: {me.first_name}")
        print(f"   • ID: {me.id}")
        print(f"   • Может присоединяться к группам: {me.can_join_groups}")
        print(f"   • Может читать все сообщения: {me.can_read_all_group_messages}")
        print()
        print(f"🔗 Ссылка на бота: https://t.me/{me.username}")
        print()
        print("📱 Откройте эту ссылку в Telegram и отправьте /start")

        return True

    except Exception as e:
        print(f"\n❌ ОШИБКА подключения к Telegram API:")
        print(f"   {e}")
        print()
        print("Возможные причины:")
        print("  1. Неверный токен")
        print("  2. Нет доступа к интернету")
        print("  3. Telegram API недоступен")
        return False

if __name__ == '__main__':
    success = test_bot_token()
    sys.exit(0 if success else 1)
