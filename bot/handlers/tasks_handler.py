# Обработка задач (добавление, изменение, наследование).
from aiogram import types
from datetime import datetime, timedelta

# Список задач (вместо базы данных, пока что временное хранение)
#hardcode
tasks = []


async def handle_add_task(message: types.Message):
    """
    Обработчик для добавления новой задачи.
    Формат команды: /addtask <описание задачи> <срок (дни)>
    """
    try:
        command_args = message.text.split(maxsplit=2)
        if len(command_args) < 3:
            await message.reply("Неверный формат команды. Используйте: /addtask <описание задачи> <срок (дни)>")
            return

        description = command_args[1]
        days = int(command_args[2])
        deadline = datetime.now() + timedelta(days=days)

        task = {
            "description": description,
            "deadline": deadline,
            "completed": False
        }
        tasks.append(task)

        await message.reply(
            f"Задача добавлена: \nОписание: {description}\nСрок: {deadline.strftime('%Y-%m-%d %H:%M:%S')}")
    except ValueError:
        await message.reply("Неверный формат. Укажите число дней корректно.")


async def handle_list_tasks(message: types.Message):
    """
    Обработчик для отображения всех задач.
    """
    if not tasks:
        await message.reply("Список задач пуст.")
        return

    response = "Ваши задачи:\n"
    for i, task in enumerate(tasks, start=1):
        status = "Выполнена" if task["completed"] else "Не выполнена"
        response += (f"{i}. {task['description']}\n"
                     f"   Срок: {task['deadline'].strftime('%Y-%m-%d %H:%M:%S')}\n"
                     f"   Статус: {status}\n")
    await message.reply(response)


async def handle_deadline_alerts(message: types.Message):
    """
    Проверяет и сообщает о приближающихся сроках задач.
    """
    now = datetime.now()
    urgent_tasks = [task for task in tasks if task["deadline"] < now + timedelta(days=1) and not task["completed"]]

    if not urgent_tasks:
        await message.reply("Нет задач с близким сроком.")
        return

    response = "Задачи с приближающимся сроком:\n"
    for task in urgent_tasks:
        response += f"- {task['description']} (до {task['deadline'].strftime('%Y-%m-%d %H:%M:%S')})\n"
    await message.reply(response)


async def handle_complete_task(message: types.Message):
    """
    Отмечает задачу как выполненную.
    Формат команды: /completetask <номер задачи>
    """
    try:
        command_args = message.text.split(maxsplit=1)
        if len(command_args) < 2:
            await message.reply("Неверный формат команды. Используйте: /completetask <номер задачи>")
            return

        task_index = int(command_args[1]) - 1
        if task_index < 0 or task_index >= len(tasks):
            await message.reply("Задача с таким номером не найдена.")
            return

        tasks[task_index]["completed"] = True
        await message.reply(f"Задача \"{tasks[task_index]['description']}\" отмечена как выполненная.")
    except ValueError:
        await message.reply("Неверный формат. Укажите номер задачи корректно.")
