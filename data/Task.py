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

    def add_task(self, category, task):
        """Добавляет задачу в указанную категорию."""
        if category in self.tasks:
            self.tasks[category].append(task)
        else:
            raise ValueError("Invalid category")

    def remove_task(self, category, task_title):
        """Удаляет задачу по названию из указанной категории."""
        if category in self.tasks:
            self.tasks[category] = [task for task in self.tasks[category] if task.title != task_title]
        else:
            raise ValueError("Invalid category")

    def get_tasks_by_category(self, category):
        """Возвращает список задач для указанной категории."""
        if category in self.tasks:
            return self.tasks[category]
        else:
            raise ValueError("Invalid category")
