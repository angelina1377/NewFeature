import csv
from typing import Any, Dict, List

import pandas as pd


def read_finance_csv_operation(file_name: str) -> List[Dict[str, Any]]:
    # Функция считывания csv файла
    result = []
    with open(file_name) as transaction_file:
        reader = csv.DictReader(transaction_file, delimiter=";")
        for row in reader:
            result.append(row)
    return result


def read_finance_excel_operation(file_path: str) -> List[Dict[str, Any]]:
    # Функция считывания Excel файла
    try:
        excel_data = pd.read_excel(file_path)
        return excel_data.to_dict("records")
    except FileNotFoundError:
        return []
    except Exception as e:
        return []
