import uuid
from datetime import datetime

class Task:
    def __init__(self, title, description, deadline, priority=1, completed=False, task_id=None):
        self.id = task_id if task_id else self.generate_task_id()
        self.title = title
        self.description = description
        self.deadline = self.parse_deadline(deadline)
        self.priority = priority
        self.completed = completed

    @staticmethod
    def generate_task_id():
        """Генерирует уникальный идентификатор задачи."""
        return f"task-{uuid.uuid4().hex[:8]}"

    @staticmethod
    def parse_deadline(deadline):
        """Преобразует строку с датой в объект datetime."""
        if isinstance(deadline, str):
            try:
                return datetime.fromisoformat(deadline)
            except ValueError:
                raise ValueError("Invalid deadline format. Expected ISO format.")
        if isinstance(deadline, datetime):
            return deadline
        raise TypeError("Deadline must be a string or datetime object.")

    def mark_as_completed(self):
        """Отмечает задачу как выполненную."""
        self.completed = True

    def to_json(self):
        """Преобразует объект задачи в JSON-совместимый словарь."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "deadline": self.deadline.isoformat(),
            "priority": self.priority,
            "completed": self.completed
        }

    @classmethod
    def from_json(cls, data):
        """Создает объект задачи из JSON-совместимого словаря."""
        required_fields = ["title", "description", "deadline"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        return cls(
            title=data["title"],
            description=data["description"],
            deadline=data["deadline"],
            priority=data.get("priority", 1),
            completed=data.get("completed", False),
            task_id=data.get("id")
        )

    def __repr__(self):
        return (f"Task(id={self.id}, title={self.title}, description={self.description}, "
                f"deadline={self.deadline}, priority={self.priority}, completed={self.completed})")


class TaskManager:
    def __init__(self, tasks_data):
        self.tasks = {
            "day": [Task.from_json(task) for task in tasks_data.get("day", [])],
            "week": [Task.from_json(task) for task in tasks_data.get("week", [])],
            "month": [Task.from_json(task) for task in tasks_data.get("month", [])],
            "other": [Task.from_json(task) for task in tasks_data.get("other", [])],
        }

    def to_json(self):
        """Конвертирует данные задач в формат JSON."""
        return {
            "day": [task.to_json() for task in self.tasks["day"]],
            "week": [task.to_json() for task in self.tasks["week"]],
            "month": [task.to_json() for task in self.tasks["month"]],
            "other": [task.to_json() for task in self.tasks["other"]],
        }

    def add_task(self, category, title, description, deadline, priority):
        """Добавляет новую задачу в указанную категорию."""
        new_task = Task(title=title, description=description, deadline=deadline, priority=priority)
        if category in self.tasks:
            self.tasks[category].append(new_task)
        else:
            raise ValueError("Invalid category")

    def update_task(self, task_id, **updates):
        """Обновляет существующую задачу по её ID."""
        for category, tasks in self.tasks.items():
            for task in tasks:
                if task.id == task_id:
                    for key, value in updates.items():
                        if hasattr(task, key):
                            setattr(task, key, value)
                    return
        raise ValueError("Task with the specified ID not found")

    def delete_task(self, task_id):
        """Удаляет задачу по её ID."""
        for category, tasks in self.tasks.items():
            for task in tasks:
                if task.id == task_id:
                    tasks.remove(task)
                    return
        raise ValueError("Task with the specified ID not found")

    def get_tasks_by_category(self, category):
        """Возвращает список задач в указанной категории."""
        if category in self.tasks:
            return self.tasks[category]
        else:
            raise ValueError("Invalid category")

    def format_tasks_message(self, category):
        """Форматирует задачи в категории для отправки сообщением."""
        if category not in self.tasks:
            raise ValueError("Invalid category")

        tasks = self.tasks[category]
        if not tasks:
            return f"Нет задач в категории {category}."

        months_rus = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"]

        message = f"{category.capitalize()}:\n"
        for task in tasks:
            status = "✔️" if task.completed else "❌"
            deadline = task.deadline
            formatted_deadline = f"{deadline.day} {months_rus[deadline.month - 1]} {deadline.hour:02}:{deadline.minute:02}"

            message += (f"{status} {task.title} ({task.id})\n"
                        f"{task.description}\n"
                        f"Дедлайн: {formatted_deadline}\n\n")
        return message
