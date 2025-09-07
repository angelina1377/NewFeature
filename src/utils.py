import json
from typing import List, Dict
from pathlib import Path


def load_operations(path: str | Path) -> List[Dict]:
    """
    Загружает и возвращает список словарей из JSON-файла.
    Возвращает [] в случаях: файл не найден, пустой, некорректный JSON, корневой элемент не список.
    """
    try:
        p = Path(path)
        if not p.exists():
            return []
        text = p.read_text(encoding="utf-8")
        if not text.strip():
            return []
        data = json.loads(text)
    except (FileNotFoundError, PermissionError, OSError, json.JSONDecodeError):
        return []

    if isinstance(data, list):
        # Возвращаем только словари, игнорируя прочие элементы в списке
        return [item for item in data if isinstance(item, dict)]
    return []


if __name__ == "__main__":
    # Путь к файлу относительно расположения этого файла (удобно при запуске из другой cwd)
    default_path = Path(__file__).resolve().parents[1] / "data" / "operations.json"
    # Можно передать абсолютный путь или оставить default_path
    ops = load_operations(default_path)

    print(f"Loaded items: {len(ops)}")
    print(f"Type: {type(ops)}")
    if ops:
        print("First items:")
        for i, op in enumerate(ops[:5], start=1):
            print(f"{i}: {op}")