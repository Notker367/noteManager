class Task:
    def __init__(self, title, deadline, priority, completed):
        self.title = title
        self.deadline = deadline
        self.priority = priority
        self.completed = completed

    @classmethod
    def from_json(cls, data):
        return cls(
            data["title"],
            data["deadline"],
            data["priority"],
            data["completed"]
        )

    def to_json(self):
        return {
            "title": self.title,
            "deadline": self.deadline,
            "priority": self.priority,
            "completed": self.completed
        }


class TaskManager:
    def __init__(self, tasks_data):
        self.tasks = {
            "day": [Task.from_json(task) for task in tasks_data.get("day", [])],
            "week": [Task.from_json(task) for task in tasks_data.get("week", [])],
            "month": [Task.from_json(task) for task in tasks_data.get("month", [])],
            "other": [Task.from_json(task) for task in tasks_data.get("other", [])],
        }

    def to_json(self):
        return {
            "day": [task.to_json() for task in self.tasks["day"]],
            "week": [task.to_json() for task in self.tasks["week"]],
            "month": [task.to_json() for task in self.tasks["month"]],
            "other": [task.to_json() for task in self.tasks["other"]],
        }

    def add_task(self, category, title, deadline, priority):
        """Добавляет новую задачу в указанную категорию."""
        new_task = Task(title, deadline, priority, False)
        if category in self.tasks:
            self.tasks[category].append(new_task)
        else:
            raise ValueError("Invalid category")

    def update_task(self, category, title, **updates):
        """Обновляет существующую задачу по названию."""
        if category in self.tasks:
            for task in self.tasks[category]:
                if task.title == title:
                    for key, value in updates.items():
                        if hasattr(task, key):
                            setattr(task, key, value)
                    break
        else:
            raise ValueError("Invalid category")

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

        message = f"Задачи в категории {category}:\n"
        for task in tasks:
            status = "✔️" if task.completed else "❌"
            message += f"{status} {task.title} (Дедлайн: {task.deadline}, Приоритет: {task.priority})\n"
        return message
