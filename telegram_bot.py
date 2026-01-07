#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Telegram бот для подсчета калорий в еде
Использует модели распознавания еды из проекта food-recognition
"""

import os
import logging
import tempfile
from typing import Dict, List
import pandas as pd

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from backend.modules import get_prediction
from backend.constants import UPLOAD_FOLDER, CSV_FOLDER, DETECTION_FOLDER


# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class CalorieBot:
    """Telegram бот для распознавания еды и подсчета калорий"""

    def __init__(self, token: str, model_name: str = 'yolov5s'):
        """
        Args:
            token: Telegram Bot API токен
            model_name: Название модели для распознавания (yolov5s, yolov5m, yolov5l, yolov8s)
        """
        self.token = token
        self.model_name = model_name
        self.application = None

        # Создаем необходимые директории
        for folder in [UPLOAD_FOLDER, DETECTION_FOLDER, CSV_FOLDER]:
            os.makedirs(folder, exist_ok=True)

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Обработчик команды /start"""
        welcome_message = (
            "🍔 Привет! Я бот для подсчета калорий.\n\n"
            "📸 Отправьте мне фотографию еды, и я:\n"
            "• Распознаю блюда на фото\n"
            "• Подсчитаю калории\n"
            "• Расскажу о содержании белков, жиров и углеводов\n\n"
            "Команды:\n"
            "/start - Показать это сообщение\n"
            "/help - Помощь\n"
            "/about - О боте\n\n"
            "Просто отправьте фото еды! 📷"
        )
        await update.message.reply_text(welcome_message)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Обработчик команды /help"""
        help_message = (
            "ℹ️ Как использовать бота:\n\n"
            "1️⃣ Сделайте фото вашей еды\n"
            "2️⃣ Отправьте фото боту\n"
            "3️⃣ Подождите несколько секунд\n"
            "4️⃣ Получите результат с калориями и питательными веществами\n\n"
            "💡 Советы:\n"
            "• Фотографируйте еду сверху для лучшего распознавания\n"
            "• Убедитесь, что блюда хорошо видны\n"
            "• Можно фотографировать несколько блюд сразу\n\n"
            "Модель распознает более 100 различных блюд! 🍕🍜🥗"
        )
        await update.message.reply_text(help_message)

    async def about_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Обработчик команды /about"""
        about_message = (
            "🤖 О боте:\n\n"
            f"Модель: {self.model_name}\n"
            "Технологии:\n"
            "• YOLOv5/YOLOv8 для обнаружения объектов\n"
            "• EfficientNet для классификации\n"
            "• Edamam API для информации о питательности\n\n"
            "Проект на GitHub:\n"
            "github.com/lannguyen0910/food-recognition\n\n"
            "Создан для помощи в подсчете калорий! 💪"
        )
        await update.message.reply_text(about_message)

    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Обработчик фотографий"""
        try:
            # Отправляем сообщение о начале обработки
            processing_msg = await update.message.reply_text(
                "🔍 Анализирую фото...\nЭто может занять несколько секунд."
            )

            # Получаем фото
            photo_file = await update.message.photo[-1].get_file()

            # Создаем временный файл для сохранения фото
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg', dir=UPLOAD_FOLDER) as tmp_input:
                input_path = tmp_input.name
                await photo_file.download_to_drive(input_path)

            # Путь для сохранения результата
            output_filename = os.path.splitext(os.path.basename(input_path))[0] + '_result.jpg'
            output_path = os.path.join(DETECTION_FOLDER, output_filename)

            # Выполняем распознавание
            logger.info(f"Processing image: {input_path}")
            result_path, task_type = get_prediction(
                input_path=input_path,
                output_path=output_path,
                model_name=self.model_name,
                tta=False,
                ensemble=False,
                min_iou=0.5,
                min_conf=0.3,
                segmentation=False,
                enhance_labels=False
            )

            # Читаем результаты из CSV
            csv_filename = os.path.splitext(os.path.basename(input_path))[0] + '_info.csv'
            csv_path = os.path.join(CSV_FOLDER, csv_filename)

            # Формируем ответ
            if os.path.exists(csv_path):
                df = pd.read_csv(csv_path)
                response_text = self._format_results(df)
            else:
                response_text = "❌ К сожалению, не удалось распознать еду на фото.\nПопробуйте другое фото."

            # Удаляем сообщение о обработке
            await processing_msg.delete()

            # Отправляем результат с фото
            if os.path.exists(output_path):
                with open(output_path, 'rb') as photo:
                    await update.message.reply_photo(
                        photo=photo,
                        caption=response_text,
                        parse_mode='HTML'
                    )
            else:
                await update.message.reply_text(response_text, parse_mode='HTML')

            # Очистка временных файлов
            self._cleanup_files(input_path, output_path, csv_path)

        except Exception as e:
            logger.error(f"Error processing photo: {e}", exc_info=True)
            await update.message.reply_text(
                "❌ Произошла ошибка при обработке фото.\n"
                "Попробуйте еще раз или отправьте другое фото."
            )

    def _format_results(self, df: pd.DataFrame) -> str:
        """Форматирует результаты распознавания в читаемый текст"""
        if len(df) == 0:
            return "❌ Еда не обнаружена на фото."

        total_calories = 0
        total_protein = 0
        total_fat = 0
        total_carbs = 0
        total_fiber = 0

        result_lines = ["✅ <b>Обнаружено на фото:</b>\n"]

        for idx, row in df.iterrows():
            name = row['names']
            calories = row.get('calories', 0) or 0
            protein = row.get('protein', 0) or 0
            fat = row.get('fat', 0) or 0
            carbs = row.get('carbs', 0) or 0
            fiber = row.get('fiber', 0) or 0

            # Переводим название с английского (базовый перевод)
            name_ru = self._translate_food_name(name)

            result_lines.append(f"\n🍽️ <b>{name_ru}</b>")
            if calories > 0:
                result_lines.append(f"   • Калории: {calories:.1f} ккал")
                result_lines.append(f"   • Белки: {protein:.1f}г")
                result_lines.append(f"   • Жиры: {fat:.1f}г")
                result_lines.append(f"   • Углеводы: {carbs:.1f}г")
                if fiber > 0:
                    result_lines.append(f"   • Клетчатка: {fiber:.1f}г")

                total_calories += calories
                total_protein += protein
                total_fat += fat
                total_carbs += carbs
                total_fiber += fiber
            else:
                result_lines.append(f"   • Нет данных о калорийности")

        if total_calories > 0:
            result_lines.append("\n" + "="*30)
            result_lines.append(f"\n📊 <b>ВСЕГО:</b>")
            result_lines.append(f"   • Калории: {total_calories:.1f} ккал")
            result_lines.append(f"   • Белки: {total_protein:.1f}г")
            result_lines.append(f"   • Жиры: {total_fat:.1f}г")
            result_lines.append(f"   • Углеводы: {total_carbs:.1f}г")
            if total_fiber > 0:
                result_lines.append(f"   • Клетчатка: {total_fiber:.1f}г")

        return "\n".join(result_lines)

    def _translate_food_name(self, name: str) -> str:
        """Базовый перевод названий еды"""
        translations = {
            'pizza': 'Пицца',
            'hamburger': 'Гамбургер',
            'sushi': 'Суши',
            'rice': 'Рис',
            'bread': 'Хлеб',
            'apple': 'Яблоко',
            'banana': 'Банан',
            'coffee': 'Кофе',
            'tea': 'Чай',
            'milk': 'Молоко',
            'cheese': 'Сыр',
            'egg': 'Яйцо',
            'fish': 'Рыба',
            'meat': 'Мясо',
            'chicken': 'Курица',
            'soup': 'Суп',
            'salad': 'Салат',
            'pasta': 'Паста',
            'noodles': 'Лапша',
            'cake': 'Торт',
            'ice cream': 'Мороженое',
            'chocolate': 'Шоколад',
            'french fries': 'Картофель фри',
            'sandwich': 'Сэндвич',
            'hot dog': 'Хот-дог',
            'steak': 'Стейк',
            'ramen': 'Рамен',
            'pho': 'Фо',
            'banh mi': 'Бань ми',
            'com tam': 'Ком там',
            'fried rice': 'Жареный рис',
        }

        name_lower = name.lower()
        return translations.get(name_lower, name.title())

    def _cleanup_files(self, *file_paths):
        """Удаляет временные файлы"""
        for file_path in file_paths:
            try:
                if file_path and os.path.exists(file_path):
                    os.remove(file_path)
                    logger.info(f"Cleaned up: {file_path}")
            except Exception as e:
                logger.warning(f"Failed to cleanup {file_path}: {e}")

    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Обработчик текстовых сообщений"""
        await update.message.reply_text(
            "📸 Пожалуйста, отправьте мне фотографию еды.\n"
            "Используйте /help для получения инструкций."
        )

    def run(self):
        """Запускает бота"""
        # Создаем приложение
        self.application = Application.builder().token(self.token).build()

        # Регистрируем обработчики команд
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("about", self.about_command))

        # Регистрируем обработчик фотографий
        self.application.add_handler(MessageHandler(filters.PHOTO, self.handle_photo))

        # Регистрируем обработчик текстовых сообщений
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text))

        # Запускаем бота
        logger.info("Bot is starting...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    """Точка входа"""
    import argparse

    parser = argparse.ArgumentParser(description='Telegram Calorie Bot')
    parser.add_argument(
        '--token',
        type=str,
        required=False,
        help='Telegram Bot API token'
    )
    parser.add_argument(
        '--model',
        type=str,
        default='yolov5s',
        choices=['yolov5s', 'yolov5m', 'yolov5l', 'yolov5x', 'yolov8s'],
        help='Model name for food detection'
    )

    args = parser.parse_args()

    # Получаем токен из аргументов или переменной окружения
    token = args.token or os.getenv('TELEGRAM_BOT_TOKEN')

    if not token:
        logger.error(
            "Please provide Telegram Bot token either via --token argument "
            "or TELEGRAM_BOT_TOKEN environment variable"
        )
        return

    # Создаем и запускаем бота
    bot = CalorieBot(token=token, model_name=args.model)
    bot.run()


if __name__ == '__main__':
    main()
