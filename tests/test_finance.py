import pytest
import os
import pandas as pd
from src.finance import read_finance_csv_operation
from src.finance import read_finance_excel_operation


def test_read_finance_csv_operation_basic():# Тест для базового csv
    # Создаем содержимое csv файла в виде строки
    csv_content = "date;amount;description\n2024-01-01;1000;Salary\n2024-01-02;-50;Groceries\n"
    file_path = "test_finance.csv" # Задаем имя файла
    # Создаем файл и записываем в него содержимое
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(csv_content)

    try:
        # Вызываем тестируемую функцию
        result = read_finance_csv_operation(file_path)
        # Создаем ожидаемый резудьтат
        expected = [
            {"date": "2024-01-01", "amount": "1000", "description": "Salary"},
            {"date": "2024-01-02", "amount": "-50", "description": "Groceries"},
        ]
        # Проверяем, что результат совпадает с ожидаемым
        assert result == expected
    finally:
        # Удаляем созданный файл после теста
        os.remove(file_path)

def test_read_finance_csv_operation_empty():# Тест для пустого csv
    # Создаем пустой csv файл с заголовками
    csv_content = "date;amount;description\n"
    file_path = "test_finance_empty.csv"
    # Создаем файл и записываем в него содержимое
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(csv_content)

    try:
        # Вызываем тестируемую функцию
        result = read_finance_csv_operation(file_path)
        # Проверяем, что результат пустой
        assert result == []
    finally:
        # Удаляем созданный файл после теста
        os.remove(file_path)


def test_read_finance_excel_operation_basic(tmp_path):
    # Создаём тестовый DataFrame
    df = pd.DataFrame([
            {"date": "2024-01-01", "amount": 100, "description": "salary"},
            {"date": "2024-01-02", "amount": -20, "description": "coffee"},
        ])
    # Создаем путь к файлу
    file_path = tmp_path / "test_finance.xlsx"
    # Сохраняем DataFrame в Excel файл
    df.to_excel(file_path, index=False)
    # Вызываем тестируемую функцию
    result = read_finance_excel_operation(str(file_path))
    # Проверяем результат
    assert result == df.to_dict("records")

def test_read_finance_excel_operation_empty(tmp_path):
    # Создаем пустой DataFrame с заголовками
    df = pd.DataFrame(columns=["date", "amount", "description"])
    # Создаем путь к файлу
    file_path = tmp_path / "test_finance_empty.xlsx"
    # Сохраняем пустой DataFrame в Excel
    df.to_excel(file_path, index=False)
    # Проверяем результат
    result = read_finance_excel_operation(str(file_path))
    assert result == []

def test_read_finance_excel_operation_missing_file():
    # Проверяем обработку отсутствующего файла
    result = read_finance_excel_operation("non_existent_file.xlsx")
    assert result == [] # Функция должна вернуть пустой список

#if __name__ == "__main__":
    #test_read_finance_csv_operation_basic()
    #test_read_finance_csv_operation_empty()
    #print("All tests passed")