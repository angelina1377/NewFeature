from unittest.mock import mock_open, patch

import pandas as pd

from src.finance import read_finance_csv_operation, read_finance_excel_operation


def test_read_finance_csv_operation_reads_csv_until_end():
    # Пример содержимого CSV; каждый ряд — словарь, как DictReader
    csv_content = "date;amount;description\n" "2025-01-01;100;income\n" "2025-01-02;200;expense\n"
    # Ожидаемые результаты после чтения
    expected = [
        {"date": "2025-01-01", "amount": "100", "description": "income"},
        {"date": "2025-01-02", "amount": "200", "description": "expense"},
    ]

    # Мокаем open и передаем содержимое файла
    m = mock_open(read_data=csv_content)

    with patch("builtins.open", m):
        with patch("csv.DictReader") as mock_dict_reader:
            # Задаем поведение DictReader: он должен возвращать итератор по словарям
            mock_dict_reader.return_value.__iter__.return_value = expected
            # Вызываем функцию
            result = read_finance_csv_operation("dummy.csv")

            # Проверяем, что результат совпадает с ожидаемым
            assert result == expected

            # Дополнительно можно проверить, что DictReader был создан с правильным delimiter
            mock_dict_reader.assert_called_once()
            args, kwargs = mock_dict_reader.call_args
            assert kwargs.get("delimiter") == ";"


def test_read_finance_excel_operation_success():
    # Подготовка данных DataFrame, который вернет pd.read_excel
    df = pd.DataFrame(
        [
            {"date": "2025-01-01", "amount": 100, "description": "income"},
            {"date": "2025-01-02", "amount": 200, "description": "expense"},
        ]
    )
    # Мок для результата to_dict("records")
    expected = [
        {"date": "2025-01-01", "amount": 100, "description": "income"},
        {"date": "2025-01-02", "amount": 200, "description": "expense"},
    ]

    with patch("pandas.read_excel", return_value=df) as mock_read_excel:
        result = read_finance_excel_operation("dummy.xlsx")
        assert result == expected
        mock_read_excel.assert_called_once_with("dummy.xlsx")


def test_read_finance_excel_operation_file_not_found():
    with patch("pandas.read_excel", side_effect=FileNotFoundError):
        result = read_finance_excel_operation("missing.xlsx")
        assert result == []


def test_read_finance_excel_operation_other_exception():
    with patch("pandas.read_excel", side_effect=Exception("boom")):
        result = read_finance_excel_operation("error.xlsx")
        assert result == []
