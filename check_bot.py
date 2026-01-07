#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Скрипт для проверки готовности Telegram бота к запуску
"""

import sys
import os

def check_dependencies():
    """Проверяет все необходимые зависимости"""
    print('🔍 Проверка зависимостей для Telegram бота...\n')

    all_ok = True

    # Список необходимых модулей
    required_modules = [
        ('telegram', 'python-telegram-bot', True),
        ('pandas', 'pandas', True),
        ('cv2', 'opencv-python-headless', True),
        ('numpy', 'numpy', True),
        ('torch', 'pytorch', True),
        ('torchvision', 'torchvision', True),
        ('gdown', 'gdown', True),
        ('tqdm', 'tqdm', True),
        ('yaml', 'pyyaml', True),
    ]

    for module_name, display_name, required in required_modules:
        try:
            mod = __import__(module_name)
            version = getattr(mod, '__version__', 'OK')
            print(f'✓ {display_name:30} {version}')
        except ImportError:
            if required:
                print(f'✗ {display_name:30} НЕ УСТАНОВЛЕН (обязательно)')
                all_ok = False
            else:
                print(f'⚠ {display_name:30} не установлен (опционально)')

    print()

    # Проверка backend модулей
    try:
        from backend.modules import get_prediction
        from backend.constants import UPLOAD_FOLDER, CSV_FOLDER, DETECTION_FOLDER
        print(f'✓ backend модули импортируются')
    except Exception as e:
        print(f'✗ backend модули: {e}')
        all_ok = False

    # Проверка telegram_bot.py
    try:
        import telegram_bot
        if hasattr(telegram_bot, 'CalorieBot'):
            print(f'✓ telegram_bot.py готов')
            print(f'✓ Класс CalorieBot доступен')
        else:
            print(f'✗ Класс CalorieBot не найден')
            all_ok = False
    except Exception as e:
        print(f'✗ telegram_bot.py: {e}')
        all_ok = False

    print()

    # Проверка конфигурации
    if os.path.exists('.env'):
        print(f'✓ Файл .env найден')

        # Проверяем токен
        with open('.env', 'r') as f:
            content = f.read()
            if 'TELEGRAM_BOT_TOKEN=' in content and 'your_bot_token_here' not in content:
                print(f'✓ Telegram Bot Token настроен')
            else:
                print(f'✗ Telegram Bot Token не настроен в .env')
                all_ok = False
    else:
        print(f'✗ Файл .env не найден')
        print(f'  Создайте его: cp .env.example .env')
        all_ok = False

    print('\n' + '='*50)

    if all_ok:
        print('\n🎉 ВСЕ ГОТОВО! Бот можно запускать!')
        print('\nЗапустите бота:')
        print('  ./run_bot.sh       (Linux/Mac)')
        print('  run_bot.bat        (Windows)')
        print('  python telegram_bot.py')
        return 0
    else:
        print('\n❌ Требуется установка недостающих компонентов')
        print('\nУстановите зависимости:')
        print('  pip install -r requirements.txt')
        return 1

if __name__ == '__main__':
    sys.exit(check_dependencies())
