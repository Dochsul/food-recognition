@echo off
REM Скрипт для запуска Telegram бота подсчета калорий (Windows)

echo 🤖 Telegram Бот для Подсчета Калорий
echo =====================================
echo.

REM Проверка наличия .env файла
if not exist .env (
    echo ⚠️  Файл .env не найден!
    echo 📝 Создайте файл .env из примера:
    echo    copy .env.example .env
    echo.
    echo 🔑 Добавьте ваш Telegram Bot Token в файл .env
    echo.
    pause
    exit /b 1
)

REM Загрузка переменных окружения из .env
for /f "usebackq tokens=1,* delims==" %%a in (".env") do (
    if not "%%a"=="" if not "%%a:~0,1%"=="#" (
        set "%%a=%%b"
    )
)

REM Проверка наличия токена
if "%TELEGRAM_BOT_TOKEN%"=="" (
    echo ❌ TELEGRAM_BOT_TOKEN не установлен!
    echo 📝 Откройте файл .env и установите правильный токен
    echo.
    pause
    exit /b 1
)

if "%TELEGRAM_BOT_TOKEN%"=="your_bot_token_here" (
    echo ❌ TELEGRAM_BOT_TOKEN не установлен!
    echo 📝 Откройте файл .env и установите правильный токен
    echo.
    pause
    exit /b 1
)

REM Проверка установки зависимостей
python -c "import telegram" 2>nul
if errorlevel 1 (
    echo 📦 Устанавливаю зависимости...
    pip install -r requirements.txt
    echo.
)

REM Запуск бота
echo 🚀 Запускаю бота...
if "%MODEL_NAME%"=="" (
    echo 📱 Модель: yolov5s (по умолчанию)
) else (
    echo 📱 Модель: %MODEL_NAME%
)
echo.

if "%MODEL_NAME%"=="" (
    python telegram_bot.py
) else (
    python telegram_bot.py --model %MODEL_NAME%
)

pause
