import json

from src.utils import load_operations
from unittest.mock import patch
from pathlib import Path

def test_file_not_exists():
    with patch.object(Path, "exists", return_value=False): # Как будто файла не существует
        assert load_operations("any/path.json") == [] # При попытке загрузить несуществцющий файл должен возвращаться пустой список

def test_empty_file():
    # Имитируем существование файла и как будто он содержит только пробел
    with patch.object(Path, "exists", return_value=True), \
         patch.object(Path, "read_text", return_value = " "):
        assert load_operations("any/path.json") == []

def test_invalid_json_():
    bad_json = "{not: valid json}" # строка с некорректным json
    with patch.object(Path, "exists", return_value=True) , \
         patch.object(Path, "read_text", return_value = bad_json): # Имитируем чтение некорректного файла
        assert  load_operations("any/path.json") == []

def test_mixed_list_filters_non_dicts(): #имитация разных типов данных
    mixed = json.dumps([{"a": 1}, 2, "x", {"b": 2}, None])
    # Имитация сущестовования файла со смешанными данными
    with patch.object(Path, "exists", return_value=True), \
         patch.object(Path, "read_text", return_value=mixed):
        assert load_operations("any/path.json") == [{"a": 1}, {"b": 2}] # Функция должна отфильтровать только словари и вернуть список словарей


def test_permission_error():
    # Имитация ошибки прав доступа при проверке существования файла
    with patch.object(Path, "exists", side_effect=PermissionError):
        assert load_operations("any/path.json") == [] # Функция должна вернуть пустой список
    # Имитация ошибки при прочтении файла и вовзращение пустого списка при этом
    with patch.object(Path, "exists", return_value=True), \
            patch.object(Path, "read_text", side_effect=PermissionError):
        assert load_operations("any/path.json") == []





