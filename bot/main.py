import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import BotCommand
from aiogram.filters import Command
import asyncio
from data_manager import messages_data, tasks_data, finances_data, save_all_data
from config import BOT_TOKEN
from handlers import tasks_handler, finance_handler, webapp_handler

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def set_commands():
    """
    Устанавливаем команды для бота, чтобы пользователи могли видеть доступные команды.
    """
    commands = [
        BotCommand(command="addtask", description="Добавить задачу"),
        BotCommand(command="addexpense", description="Добавить расход"),
        BotCommand(command="webapp", description="Открыть Web App"),
        BotCommand(command="listtasks", description="Показать список задач"),
        BotCommand(command="financereport", description="Финансовый отчет"),
    ]
    await bot.set_my_commands(commands)


# Регистрация обработчиков (handlers)
async def on_startup():
    """
    Действия при запуске бота.
    Здесь можно настроить логи, команды и подключение к базе данных.
    """
    logger.info("Bot is starting...")
    logger.info("Загружаем данные:")
    logger.info(f"Сообщения: {len(messages_data)} записей загружено")
    logger.info(f"Задачи: {len(tasks_data)} записей загружено")
    logger.info(f"Финансы: {len(finances_data)} записей загружено")
    await set_commands()  # Установка списка команд


def register_handlers():
    """
    Регистрация всех обработчиков для команд и сообщений.
    """
    # Обработчик команды /addtask - добавление новой задачи
    dp.message.register(tasks_handler.handle_add_task, Command(commands=['addtask']))

    # Обработчик команды /addexpense - добавление нового расхода
    dp.message.register(finance_handler.handle_add_expense, Command(commands=['addexpense']))

    # Обработчик команды /webapp - открытие Telegram Web App
    dp.message.register(webapp_handler.handle_webapp, Command(commands=['webapp']))

    # Обработчик команды /listtasks - получение списка задач
    dp.message.register(tasks_handler.handle_list_tasks, Command(commands=['listtasks']))

    # Обработчик команды /financereport - финансовый отчет
    dp.message.register(finance_handler.handle_finance_report, Command(commands=['financereport']))

    # Обработчик напоминаний о дедлайнах задач (например, ежедневная проверка)
    dp.message.register(tasks_handler.handle_deadline_alerts)


async def main():
    """
    Основная асинхронная функция для запуска бота.
    """
    register_handlers()  # Регистрация обработчиков
    await on_startup()  # Выполнение действий при старте

    # Запуск polling для обработки обновлений
    logger.info("Starting polling...")
    try:
        await dp.start_polling(bot)
    finally:
        logger.info("Сохраняем данные перед завершением работы...")
        save_all_data()


if __name__ == "__main__":
    asyncio.run(main())
