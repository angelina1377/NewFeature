import csv
import pandas as pd
from typing import Any, Dict, List


def read_finance_csv_operation(file_name: str) -> List[Dict[str,Any]]:
    # Функция считывания csv файла
    result = []
    with open(file_name) as transaction_file:
        reader = csv.DictReader(transaction_file, delimiter=";")
        for row in reader:
            result.append(row)
    return result


def read_finance_excel_operation(file_path: str) -> List[Dict[str,Any]]:
    # Функция считывания
    try:
        excel_data = pd.read_excel(file_path)
        return excel_data.to_dict("records")
    except FileNotFoundError:
        return []
    except Exception as e:
        return []


# print(read_finance_csv_operation("./data/transactions.csv"))
# print(read_finance_excel_operation("../data/transactions_excel.xlsx"))
