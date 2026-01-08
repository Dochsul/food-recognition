# 📱 Запуск бота с телефона

## ✅ Вариант 1: Termux (Android) - РАБОТАЕТ!

**Termux** - терминал Linux для Android. Можно запустить Python прямо на телефоне!

### Шаг 1: Установка Termux

1. Скачайте **Termux** из F-Droid: https://f-droid.org/en/packages/com.termux/

   ⚠️ **НЕ СТАВЬТЕ из Google Play** - там старая версия!

### Шаг 2: Установка Python и зависимостей

Откройте Termux и введите команды:

```bash
# Обновите пакеты
pkg update && pkg upgrade -y

# Установите необходимые пакеты
pkg install python git -y

# Установите pip
pip install --upgrade pip

# Дайте разрешение на хранилище (для сохранения файлов)
termux-setup-storage
```

### Шаг 3: Клонируйте репозиторий

```bash
# Перейдите в storage
cd ~/storage/shared

# Клонируйте проект
git clone https://github.com/Dochsul/food-recognition.git
cd food-recognition
git checkout claude/telegram-calorie-bot-S1cQy
```

### Шаг 4: Простая версия (БЕЗ моделей) - для теста

```bash
# Установите только telegram библиотеку
pip install python-telegram-bot

# Запустите тестового бота
python simple_test_bot.py --token 8208188455:AAGa25OfMqTvM2bfhVIQkvwht2xvG8oDEmI
```

Если видите `✅ Бот запущен!` - откройте Telegram и напишите боту!

### Шаг 5: Полная версия (С моделями) - может не запуститься на слабых телефонах

```bash
# Установите зависимости (займет 20-30 минут и ~2GB)
pip install -r requirements.txt

# Запустите бота
python telegram_bot.py --token 8208188455:AAGa25OfMqTvM2bfhVIQkvwht2xvG8oDEmI
```

⚠️ **Внимание:**
- Нужно минимум 4GB RAM на телефоне
- Разрядит батарею быстро
- Телефон будет греться
- Не закрывайте Termux пока бот работает

### Фоновый запуск в Termux:

```bash
# Установите tmux для фонового запуска
pkg install tmux

# Запустите tmux сессию
tmux

# Запустите бота
python simple_test_bot.py --token 8208188455:AAGa25OfMqTvM2bfhVIQkvwht2xvG8oDEmI

# Отключитесь от сессии: Ctrl+B, затем D
# Вернуться к сессии: tmux attach
```

---

## ✅ Вариант 2: Replit.com (РЕКОМЕНДУЕТСЯ для телефона!)

**Лучший вариант** - использовать облачный IDE прямо из браузера телефона!

### Шаг 1: Зарегистрируйтесь

1. Откройте https://replit.com на телефоне
2. Зарегистрируйтесь (можно через Google/GitHub)

### Шаг 2: Создайте Repl

1. Нажмите **+ Create Repl**
2. Выберите **Import from GitHub**
3. Вставьте: `https://github.com/Dochsul/food-recognition`
4. Branch: `claude/telegram-calorie-bot-S1cQy`
5. Нажмите **Import from GitHub**

### Шаг 3: Настройте токен

1. Слева нажмите **Secrets** (замок 🔒)
2. Создайте новый секрет:
   - Key: `TELEGRAM_BOT_TOKEN`
   - Value: `8208188455:AAGa25OfMqTvM2bfhVIQkvwht2xvG8oDEmI`

### Шаг 4: Запустите

В файле `.replit` измените команду run на:

```toml
run = "python simple_test_bot.py"
```

Или для полной версии:

```toml
run = "python telegram_bot.py"
```

Нажмите **Run** ▶️

### Важно:
- Бесплатный план Replit выключает приложения если неактивны 1 час
- Для постоянной работы - платный план $7/месяц
- Но для тестирования - идеально!

---

## ✅ Вариант 3: GitHub Codespaces (Бесплатно 60 часов/месяц)

1. Откройте https://github.com/Dochsul/food-recognition
2. Нажмите **Code** → **Codespaces** → **Create codespace**
3. Дождитесь загрузки
4. В терминале:

```bash
git checkout claude/telegram-calorie-bot-S1cQy
pip install python-telegram-bot
python simple_test_bot.py --token 8208188455:AAGa25OfMqTvM2bfhVIQkvwht2xvG8oDEmI
```

---

## ✅ Вариант 4: Pythonanywhere.com

1. Зарегистрируйтесь на https://www.pythonanywhere.com
2. Бесплатный план дает постоянно работающий бот!
3. В консоли:

```bash
git clone https://github.com/Dochsul/food-recognition.git
cd food-recognition
git checkout claude/telegram-calorie-bot-S1cQy
pip install --user python-telegram-bot
python simple_test_bot.py --token 8208188455:AAGa25OfMqTvM2bfhVIQkvwht2xvG8oDEmI
```

4. Создайте **Always-on task** в настройках

---

## 📱 iOS (iPhone/iPad)

К сожалению, на iOS нет Termux. Используйте облачные варианты:

1. **Replit** (рекомендуется)
2. **GitHub Codespaces**
3. **Pythonanywhere**

Все они работают из браузера Safari!

---

## 🔋 Советы для экономии батареи на Android

Если запускаете в Termux:

```bash
# 1. Используйте Termux:Boot для автозапуска

# 2. Включите Wakelock в Termux
termux-wake-lock

# 3. Отключите неиспользуемые сервисы
# Используйте простую версию бота без моделей!
```

---

## ⚡ Быстрый старт (1 минута)

**Самый быстрый способ попробовать:**

1. Откройте https://replit.com на телефоне
2. Войдите через Google
3. Нажмите **+ Create** → **Python**
4. Скопируйте-вставьте код:

```python
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('🍔 Привет! Я работаю!')

app = Application.builder().token("8208188455:AAGa25OfMqTvM2bfhVIQkvwht2xvG8oDEmI").build()
app.add_handler(CommandHandler("start", start))

print("✅ Бот запущен!")
app.run_polling()
```

5. Нажмите **Run**
6. Откройте Telegram → @my_calorietracker_bot → /start

---

## 📞 Что делать если:

### "Бот не отвечает"
- Проверьте работает ли скрипт (есть ли `✅ Бот запущен!`)
- Подождите 10-15 секунд
- Попробуйте /start снова

### "No module named telegram"
```bash
pip install python-telegram-bot
```

### "Out of memory" на телефоне
- Закройте другие приложения
- Используйте `simple_test_bot.py` вместо `telegram_bot.py`
- Или используйте облачный вариант (Replit)

### Телефон сильно греется
- Это нормально для полной версии с моделями
- Используйте простую версию `simple_test_bot.py`
- Или переключитесь на облачный хостинг

---

## 🎯 Рекомендация

**Для телефона лучше использовать облачные варианты:**

1. **Replit.com** - проще всего, работает из браузера
2. **Pythonanywhere** - бесплатно постоянно
3. **Termux** - только если хотите полный контроль

**НЕ рекомендуется** запускать полную версию с моделями на телефоне - слишком тяжело.

Используйте `simple_test_bot.py` для теста или облачный хостинг для постоянной работы!

---

Готово! 🚀
