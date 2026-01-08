# 🚀 Руководство по развертыванию Telegram бота

## ⚠️ ВАЖНО

Бот **НЕ МОЖЕТ работать** в окружениях с ограниченным доступом к Telegram API (ошибка 403 Forbidden). Вам нужно развернуть его на машине/сервере с доступом к интернету.

## 🎯 Быстрый тест (БЕЗ моделей распознавания)

Сначала протестируйте простую версию без тяжелых моделей:

```bash
# Клонируйте репозиторий
git clone https://github.com/Dochsul/food-recognition.git
cd food-recognition
git checkout claude/telegram-calorie-bot-S1cQy

# Установите только telegram библиотеку
pip install python-telegram-bot

# Запустите тестового бота
python simple_test_bot.py --token 8208188455:AAGa25OfMqTvM2bfhVIQkvwht2xvG8oDEmI
```

Если видите `✅ Бот запущен и работает!` - значит все ок!

Откройте Telegram → @my_calorietracker_bot → /start

---

## 📱 Вариант 1: Локальный компьютер (Windows/Mac/Linux)

### Требования:
- Python 3.8+
- ~3GB свободного места
- Доступ к интернету

### Установка:

```bash
# 1. Клонируйте репозиторий
git clone https://github.com/Dochsul/food-recognition.git
cd food-recognition
git checkout claude/telegram-calorie-bot-S1cQy

# 2. Создайте виртуальное окружение (опционально, но рекомендуется)
python -m venv venv

# Активация:
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Установите зависимости (занимает 10-15 мин)
pip install -r requirements.txt

# 4. Запустите бота
python telegram_bot.py --token 8208188455:AAGa25OfMqTvM2bfhVIQkvwht2xvG8oDEmI
```

### При первом запуске:
- Загрузка моделей (~50-200MB)
- Инициализация займет 1-2 минуты
- Не закрывайте окно терминала

---

## ☁️ Вариант 2: Бесплатный облачный хостинг

### 2.1. Railway.app (РЕКОМЕНДУЕТСЯ)

**Преимущества:** $5 бесплатно в месяц, автоматическое развертывание

```bash
# 1. Зарегистрируйтесь на https://railway.app
# 2. Подключите ваш GitHub репозиторий
# 3. Создайте новый проект из репозитория
# 4. Добавьте переменную окружения:
#    TELEGRAM_BOT_TOKEN=8208188455:AAGa25OfMqTvM2bfhVIQkvwht2xvG8oDEmI
# 5. Нажмите Deploy
```

Создайте файл `Procfile` в корне репозитория:
```
worker: python telegram_bot.py
```

### 2.2. Render.com

**Преимущества:** Полностью бесплатный план

1. Зайдите на https://render.com
2. Создайте **Web Service**
3. Подключите GitHub репозиторий
4. Настройки:
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python telegram_bot.py`
5. Добавьте переменную окружения `TELEGRAM_BOT_TOKEN`
6. Deploy!

### 2.3. Fly.io

```bash
# 1. Установите Fly CLI
curl -L https://fly.io/install.sh | sh

# 2. Войдите
fly auth login

# 3. Создайте приложение
fly launch

# 4. Установите переменные
fly secrets set TELEGRAM_BOT_TOKEN=8208188455:AAGa25OfMqTvM2bfhVIQkvwht2xvG8oDEmI

# 5. Deploy
fly deploy
```

Создайте `fly.toml`:
```toml
app = "calorie-bot"

[build]
  builder = "paketobuildpacks/builder:base"

[[services]]
  internal_port = 8080
  protocol = "tcp"

  [[services.ports]]
    port = 80
```

---

## 🐳 Вариант 3: Docker

### Создайте Dockerfile:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY . .

# Переменные окружения
ENV TELEGRAM_BOT_TOKEN=""

# Запуск
CMD ["python", "telegram_bot.py"]
```

### Запуск:

```bash
# Сборка
docker build -t calorie-bot .

# Запуск
docker run -e TELEGRAM_BOT_TOKEN=8208188455:AAGa25OfMqTvM2bfhVIQkvwht2xvG8oDEmI calorie-bot
```

---

## 🖥️ Вариант 4: VPS (DigitalOcean, Linode, AWS)

Если у вас есть VPS:

```bash
# SSH в ваш сервер
ssh user@your-server-ip

# Установите Python 3.8+
sudo apt update
sudo apt install python3 python3-pip git

# Клонируйте репозиторий
git clone https://github.com/Dochsul/food-recognition.git
cd food-recognition
git checkout claude/telegram-calorie-bot-S1cQy

# Установите зависимости
pip3 install -r requirements.txt

# Запустите в фоне с nohup
nohup python3 telegram_bot.py --token 8208188455:AAGa25OfMqTvM2bfhVIQkvwht2xvG8oDEmI > bot.log 2>&1 &

# Или используйте systemd service (рекомендуется)
# Создайте /etc/systemd/system/calorie-bot.service:
```

```ini
[Unit]
Description=Calorie Counter Telegram Bot
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/path/to/food-recognition
Environment="TELEGRAM_BOT_TOKEN=8208188455:AAGa25OfMqTvM2bfhVIQkvwht2xvG8oDEmI"
ExecStart=/usr/bin/python3 telegram_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Включите и запустите service
sudo systemctl enable calorie-bot
sudo systemctl start calorie-bot
sudo systemctl status calorie-bot
```

---

## ✅ Проверка работы

1. **Найдите бота в Telegram:** @my_calorietracker_bot
2. **Отправьте:** `/start`
3. **Вы должны получить приветствие**
4. **Отправьте фото еды**
5. **Подождите 5-10 секунд**
6. **Получите результат!**

---

## 🐛 Решение проблем

### Бот не отвечает в Telegram

```bash
# Проверьте логи
tail -f bot.log

# Убедитесь что процесс запущен
ps aux | grep telegram_bot.py

# Проверьте подключение к Telegram
python test_bot_connection.py
```

### Ошибка "403 Forbidden"

**Причина:** Нет доступа к api.telegram.org

**Решение:** Запустите на другой машине/сервере с доступом к интернету

### Ошибка импорта модулей

```bash
# Переустановите зависимости
pip install --upgrade -r requirements.txt
```

### Бот зависает при обработке фото

**Нормально!** Первая обработка занимает 1-2 минуты (загрузка моделей).
Следующие фото обрабатываются за 5-10 секунд.

### Out of Memory

Используйте более легкую модель:
```bash
python telegram_bot.py --model yolov5s --token YOUR_TOKEN
```

---

## 📊 Использование ресурсов

| Модель | RAM | Размер | Скорость | Точность |
|--------|-----|--------|----------|----------|
| yolov5s | ~2GB | 28MB | Быстро | Хорошо |
| yolov5m | ~3GB | 84MB | Средне | Отлично |
| yolov5l | ~4GB | 189MB | Медленно | Лучше |
| yolov8s | ~2GB | 22MB | Быстро | Отлично |

**Рекомендуется:** yolov5s или yolov8s

---

## 🔒 Безопасность

- ❌ НЕ публикуйте токен в открытый доступ
- ✅ Используйте переменные окружения
- ✅ Добавьте `.env` в `.gitignore`
- ✅ Регулярно обновляйте зависимости

---

## 📞 Поддержка

- Документация: `TELEGRAM_BOT.md`
- Установка: `INSTALL_GUIDE.md`
- Проверка: `python check_bot.py`
- Тест: `python test_bot_connection.py`

---

**Успехов! 🚀**
