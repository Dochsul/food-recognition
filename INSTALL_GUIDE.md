# 🔧 Руководство по установке Telegram бота

## ✅ Что уже настроено:

- ✓ Код бота (`telegram_bot.py`)
- ✓ Конфигурация (`.env` с токеном)
- ✓ Документация (`TELEGRAM_BOT.md`)
- ✓ Скрипты запуска

## 📦 Установка зависимостей:

### Метод 1: Автоматическая установка

```bash
# Установить все зависимости разом
pip install -r requirements.txt
```

###  Метод 2: Пошаговая установка

Если автоматическая установка занимает слишком много времени:

```bash
# 1. Основные библиотеки (быстро)
pip install python-telegram-bot pandas opencv-python-headless "numpy<2"

# 2. PyTorch CPU версия (может занять 5-10 мин)
pip install torch torchvision --extra-index-url https://download.pytorch.org/whl/cpu

# 3. Остальные зависимости
pip install gdown tqdm pyyaml ultralytics timm albumentations omegaconf
```

## 🔍 Проверка готовности:

```bash
python check_bot.py
```

Ожидаемый вывод:
```
✓ python-telegram-bot       22.5
✓ pandas                    2.3.3
✓ opencv                    4.7.0
✓ numpy                     1.26.4
✓ pytorch                   2.x.x
...
🎉 ВСЕ ГОТОВО! Бот можно запускать!
```

## 🚀 Запуск бота:

### Вариант 1: Через скрипты

```bash
# Linux/Mac
./run_bot.sh

# Windows
run_bot.bat
```

### Вариант 2: Напрямую

```bash
python telegram_bot.py
```

С выбором модели:
```bash
python telegram_bot.py --model yolov5s    # Быстрая
python telegram_bot.py --model yolov5l    # Более точная
python telegram_bot.py --model yolov8s    # Новая версия
```

## 📱 Использование бота:

1. Найдите вашего бота в Telegram: **@my_calorietracker_bot**
2. Отправьте `/start`
3. Отправьте фото еды
4. Получите результат с калориями!

## ❓ Решение проблем:

### Ошибка "No module named 'torch'"

```bash
# Убедитесь что PyTorch установлен
python -c "import torch; print(torch.__version__)"

# Если нет - установите
pip install torch torchvision --extra-index-url https://download.pytorch.org/whl/cpu
```

### Ошибка "numpy.core.multiarray failed to import"

```bash
# Понизьте версию numpy
pip install "numpy<2"
```

### Бот не запускается - "токен неверный"

1. Проверьте файл `.env`
2. Убедитесь что токен скопирован правильно (без пробелов)
3. Получите новый токен у @BotFather если нужно

### Медленная работа бота

1. Используйте более легкую модель: `--model yolov5s`
2. Уменьшите параметры в `telegram_bot.py`:
   - `min_conf=0.4` (вместо 0.3)
   - `tta=False`
   - `ensemble=False`

## 💡 Полезные команды:

```bash
# Проверить установленные пакеты
pip list | grep -E "(torch|telegram|pandas|opencv)"

# Обновить зависимости
pip install --upgrade -r requirements.txt

# Посмотреть логи бота (если запущен в фоне)
tail -f bot.log

# Остановить бота
# Ctrl+C или pkill -f telegram_bot.py
```

## 📚 Дополнительная информация:

- Полная документация: `TELEGRAM_BOT.md`
- Код бота: `telegram_bot.py`
- Проверка: `python check_bot.py`

## 🆘 Поддержка:

Если возникли проблемы:
1. Проверьте `python check_bot.py`
2. Прочитайте `TELEGRAM_BOT.md`
3. Создайте issue на GitHub

---

Удачи! 🚀
