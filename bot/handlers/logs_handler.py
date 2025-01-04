# Логирование.
import logging

# Настройка логирования
logger = logging.getLogger("bot_logger")


def setup_logging():
    """
    Настраивает логирование для бота.
    """
    # Создаем обработчик для вывода логов в консоль
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Создаем обработчик для записи логов в файл
    file_handler = logging.FileHandler("bot.log", encoding="utf-8")
    file_handler.setLevel(logging.INFO)

    # Формат логов
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Добавляем обработчики к логгеру
    logger.setLevel(logging.INFO)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.info("Логирование настроено.")


def log_message(message):
    """
    Логирует текст сообщения от пользователя.
    :param message: Объект сообщения от aiogram
    """
    user_id = message.from_user.id
    username = message.from_user.username or "unknown"
    text = message.text

    logger.info(f"Сообщение от {username} (ID: {user_id}): {text}")
