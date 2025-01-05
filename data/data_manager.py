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
            with open(file_path, "r", encoding="utf-8") as j_file:
                return json.load(j_file)
        return {}  # Возвращаем пустой словарь, если файл не найден

    @staticmethod
    def save(file_path, data):
        """Сохраняет данные в JSON файл."""
        with open(file_path, "w", encoding="utf-8") as j_file:
            json.dump(data, j_file, indent=4, ensure_ascii=False)


# Инициализация файлов
for file in [messages_file, tasks_file, finances_file]:
    if not file.exists():
        JSONManager.save(file, {})

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
