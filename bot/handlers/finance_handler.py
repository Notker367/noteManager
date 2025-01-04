# Обработка финансовых данных.
import logging
from aiogram import types

# Настройка логирования
logger = logging.getLogger(__name__)

# Временное хранилище для расходов (можно заменить на базу данных)
expenses = []


async def handle_add_expense(message: types.Message):
    """
    Обработчик команды /addexpense для добавления нового расхода.
    Формат команды: /addexpense <сумма> <категория>
    """
    try:
        # Разбиваем текст команды на части
        parts = message.text.split(maxsplit=2)
        if len(parts) < 3:
            await message.reply("Неверный формат. Используйте: /addexpense <сумма> <категория>")
            return

        amount = float(parts[1])  # Парсим сумму
        category = parts[2]  # Получаем категорию

        # Сохраняем расход в списке
        expenses.append({
            "amount": amount,
            "category": category,
            "user": message.from_user.id,
        })

        logger.info(f"Добавлен расход: {amount} ({category}) от пользователя {message.from_user.id}")
        await message.reply(f"Добавлен расход: {amount} ({category})")

    except ValueError:
        await message.reply("Ошибка: сумма должна быть числом. Используйте: /addexpense <сумма> <категория>")


async def handle_finance_report(message: types.Message):
    """
    Обработчик команды /financereport для вывода отчета о расходах.
    """
    user_expenses = [e for e in expenses if e["user"] == message.from_user.id]

    if not user_expenses:
        await message.reply("У вас пока нет записанных расходов.")
        return

    # Генерация отчета
    report_lines = [
        f"{i + 1}. {e['amount']} - {e['category']}"
        for i, e in enumerate(user_expenses)
    ]
    report = "\n".join(report_lines)

    await message.reply(f"Ваши расходы:\n{report}")
