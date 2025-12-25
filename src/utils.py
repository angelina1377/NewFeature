import json
import logging
from pathlib import Path
from typing import Dict, List, Union
from datetime import datetime


# Настройка логирования
def setup_logging() -> None:
    # Создаем директорию для логов, если её нет
    logs_dir = Path(__file__).resolve().parents[1] / "logs"
    # Path(__file__) - получает путь к текущему исполняемому файлу (скрипт, в котором написан этот код)
    # .resolve() - преобразует относительный путь в абсолютный
    # .parents[1] - поднимается на два уровня вверх по директори
    # / "logs" - добавляет к полученному пути папку “logs”
    logs_dir.mkdir(parents=True, exist_ok=True) # Создание директории с 2 параметрами
    # parents=True - создает все необходимые родительские директории, если их нет
    # exist_ok=True - не вызывает ошибку, если директория уже существует

    # Формируем имя файла лога с текущей датой
    log_filename = logs_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"
    # logs_dir - путь к директории логов
    # datetime.now() - получает текущую дату
    # .strftime('%Y%m%d') - форматирует дату
    # Итоговый файл будет иметь имя вида app_20250911.log

    # Настраиваем логгер
    logging.basicConfig(
        filename=log_filename, # Путь к файлу лога
        level=logging.DEBUG, # Уровень логирования
        format="%(asctime)s - %(module)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S", # Формат даты
    )

    # Очищаем файл лога при каждом запуске
    with open(log_filename, "w") as file:
        pass


def load_operations(path: Union[str | Path]) -> List[Dict]:
    """
    Загружает и возвращает список словарей из JSON-файла.
    Возвращает [] в случаях: файл не найден, пустой, некорректный JSON, корневой элемент не список.
    """
    try:
        p = Path(path) # Преобразуем путь в объект Path
        if not p.exists(): # Проверяем существование файла
            logging.warning(f"File not found: {p}")
            return []
        text = p.read_text(encoding="utf-8") # Читаем содержимое файла
        if not text.strip(): # Проверяем на пустоту
            logging.warning(f"Empty file: {p}")
            return []
        data = json.loads(text) # Парсим JSON
    except (FileNotFoundError, PermissionError, OSError, json.JSONDecodeError) as e:
        logging.error(f"Error reading file {p}: {str(e)}")
        return []

    if isinstance(data, list): # Проверяем, что данные - список
        # Возвращаем только словари, игнорируя прочие элементы в списке
        logging.info(f"Successfully loaded {len(data)} items from {p}")
        return [item for item in data if isinstance(item, dict)] # Возвращаем только словари
    logging.warning(f"Data is not a list in file {p}")
    return []


if __name__ == "__main__":
    setup_logging() # Настраиваем логирование
    logger = logging.getLogger(__name__) # Получаем логгер

    # Тестовые логи разных уровней
    logger.debug("Это тестовое сообщение уровня DEBUG")
    logger.info("Это тестовое сообщение уровня INFO")
    logger.warning("Это тестовое предупреждение")
    logger.error("Это тестовая ошибка")

    # Тестирование функции load_operations
    test_path = "test_data.json"  # Путь к тестовому файлу
    load_operations(test_path)
