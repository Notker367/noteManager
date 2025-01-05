from aiogram import types
from datetime import datetime, timedelta
from data.Task import TaskManager, Task
from data.data_manager import tasks_data

# Инициализация TaskManager
tasks_manager = TaskManager(tasks_data=tasks_data)


async def handle_add_task(message: types.Message):
    """
    Обработчик для добавления новой задачи.
    Формат команды: /addtask <категория> <название> <срок (дни)> <описание>
    """
    try:
        command_args = message.text.split(maxsplit=4)
        if len(command_args) < 5:
            await message.reply(
                "Неверный формат команды. Используйте: /addtask <категория> <название> <срок (дни)> <описание>")
            return

        category = command_args[1]
        title = command_args[2]
        days = int(command_args[3])
        description = command_args[4]
        deadline = datetime.now() + timedelta(days=days)

        tasks_manager.add_task(category, title, description, deadline, priority=1)
        await message.reply(f"Задача \"{title}\" успешно добавлена в категорию \"{category}\".")
    except ValueError:
        await message.reply("Неверный формат. Укажите число дней корректно.")
    except Exception as e:
        await message.reply(f"Ошибка: {str(e)}")


async def handle_list_tasks(message: types.Message):
    """
    Обработчик для отображения всех задач в указанной категории.
    """
    command_args = message.text.split(maxsplit=1)
    category = command_args[1] if len(command_args) > 1 else "day"  # Категория по умолчанию - "day"

    try:
        tasks_message = tasks_manager.format_tasks_message(category)
        await message.reply(tasks_message)
    except ValueError as e:
        await message.reply(str(e))


async def handle_complete_task(message: types.Message):
    """
    Обработчик для отметки задачи как выполненной.
    Формат команды: /completetask <ID задачи>
    """
    try:
        command_args = message.text.split(maxsplit=1)
        if len(command_args) < 2:
            await message.reply("Неверный формат команды. Используйте: /completetask <ID задачи>")
            return

        task_id = command_args[1]
        tasks_manager.update_task(task_id, completed=True)
        await message.reply(f"Задача с ID {task_id} отмечена как выполненная.")
    except ValueError as e:
        await message.reply(str(e))


async def handle_delete_task(message: types.Message):
    """
    Обработчик для удаления задачи.
    Формат команды: /deletetask <ID задачи>
    """
    try:
        command_args = message.text.split(maxsplit=1)
        if len(command_args) < 2:
            await message.reply("Неверный формат команды. Используйте: /deletetask <ID задачи>")
            return

        task_id = command_args[1]
        tasks_manager.delete_task(task_id)
        await message.reply(f"Задача с ID {task_id} успешно удалена.")
    except ValueError as e:
        await message.reply(str(e))
