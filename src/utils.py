import json
import logging
from pathlib import Path
from typing import Dict, List, Union
from datetime import datetime


# Настройка логирования
def setup_logging() -> None:
    # Создаем директорию для логов, если её нет
    logs_dir = Path(__file__).resolve().parents[1] / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    # Формируем имя файла лога с текущей датой
    log_filename = logs_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"

    # Настраиваем логгер
    logging.basicConfig(
        filename=log_filename,
        level=logging.DEBUG,
        format="%(asctime)s - %(module)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
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
        p = Path(path)
        if not p.exists():
            logging.warning(f"File not found: {p}")
            return []
        text = p.read_text(encoding="utf-8")
        if not text.strip():
            logging.warning(f"Empty file: {p}")
            return []
        data = json.loads(text)
    except (FileNotFoundError, PermissionError, OSError, json.JSONDecodeError) as e:
        logging.error(f"Error reading file {p}: {str(e)}")
        return []

    if isinstance(data, list):
        # Возвращаем только словари, игнорируя прочие элементы в списке
        logging.info(f"Successfully loaded {len(data)} items from {p}")
        return [item for item in data if isinstance(item, dict)]
    logging.warning(f"Data is not a list in file {p}")
    return []


if __name__ == "__main__":
    setup_logging()
    logger = logging.getLogger(__name__)

    # Тестовые логи разных уровней
    logger.debug("Это тестовое сообщение уровня DEBUG")
    logger.info("Это тестовое сообщение уровня INFO")
    logger.warning("Это тестовое предупреждение")
    logger.error("Это тестовая ошибка")

    # Тестирование функции load_operations
    test_path = "test_data.json"  # Создан пустой файл
    load_operations(test_path)
