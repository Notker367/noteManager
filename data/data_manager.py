import json
from pathlib import Path
import atexit

# Определяем путь к папке data
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)  # Создаем папку, если её нет

# Определяем пути к JSON-файлам
messages_file = data_dir / "messages.json"
tasks_file = data_dir / "tasks.json"
finances_file = data_dir / "finances.json"


# Утилиты для работы с JSON
class JSONManager:
    @staticmethod
    def load(file_path):
        """Загружает данные из JSON файла."""
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        return []  # Возвращаем пустой список, если файл не найден

    @staticmethod
    def save(file_path, data):
        """Сохраняет данные в JSON файл."""
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


# Классы для работы с данными

class Message:
    def __init__(self, text, timestamp):
        self.text = text
        self.timestamp = timestamp

    @classmethod
    def from_json(cls, data):
        return cls(data["text"], data["timestamp"])

    def to_json(self):
        return {
            "text": self.text,
            "timestamp": self.timestamp
        }


class Task:
    def __init__(self, title, deadline, completed):
        self.title = title
        self.deadline = deadline
        self.completed = completed

    @classmethod
    def from_json(cls, data):
        return cls(data["title"], data["deadline"], data["completed"])

    def to_json(self):
        return {
            "title": self.title,
            "deadline": self.deadline,
            "completed": self.completed
        }


class Finance:
    def __init__(self, amount, category, timestamp):
        self.amount = amount
        self.category = category
        self.timestamp = timestamp

    @classmethod
    def from_json(cls, data):
        return cls(data["amount"], data["category"], data["timestamp"])

    def to_json(self):
        return {
            "amount": self.amount,
            "category": self.category,
            "timestamp": self.timestamp
        }


# Инициализация файлов
for file in [messages_file, tasks_file, finances_file]:
    if not file.exists():
        JSONManager.save(file, [])

# Глобальные переменные для хранения данных
messages_data = JSONManager.load(messages_file)
tasks_data = JSONManager.load(tasks_file)
finances_data = JSONManager.load(finances_file)


# Функция для сохранения данных при завершении работы
def save_all_data():
    JSONManager.save(messages_file, messages_data)
    JSONManager.save(tasks_file, tasks_data)
    JSONManager.save(finances_file, finances_data)


# Регистрация функции сохранения при завершении процесса
atexit.register(save_all_data)
