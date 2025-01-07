import logging
from aiogram import types
from aiogram.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
from bot.config import WEB_APP_URL

# Настройка логирования
logger = logging.getLogger(__name__)


async def handle_webapp(message: types.Message):
    """
    Обработчик команды /webapp для открытия Telegram Web App.
    """
    try:
        # Указываем URL Web App
        web_app_url = WEB_APP_URL

        # Создаем кнопку с Web App
        keyboard = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text="Открыть Web App", web_app=WebAppInfo(url=web_app_url))]
        ], resize_keyboard=True)

        logger.info(f"Пользователю {message.from_user.id} отправлена кнопка Web App")

        # Отправляем сообщение с кнопкой
        await message.answer("Нажмите на кнопку ниже, чтобы открыть Web App:", reply_markup=keyboard)

    except Exception as e:
        logger.error(f"Ошибка при обработке команды /webapp: {e}")
        await message.answer("Произошла ошибка при открытии Web App. Попробуйте позже.")
