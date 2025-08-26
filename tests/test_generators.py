import pytest

from src.generators import filter_by_currency

@pytest.mark.parametrize(
    "currency, expected_ids",
    [
        ("USD", [939719570, 142264268]),
        ("RUB", [873106923, 594226727]),
        ("EUR", []),
        ("USD", [939719570, 142264268]),
        ("XYZ", [])

    ]
)
def test_filter_by_currency(currency, expected_ids):#Фильтрация
    #Получаем отфильтрованные транзакции
    filtered_transactions = list(filter_by_currency(transactions_data, currency))
    #Извлекаем id из полученных транзакций
    result_ids = [tx["id"] for tx in filtered_transactions]
    #Проверяем соответствие
    assert result_ids == expected_ids, f"Неверный результат для валюты {currency}"

    #Дополнительный тест для пустой коллекции
def test_empty_transactions():
    empty_transactions =[]
    result = list(filter_by_currency(empty_transactions, "USD"))
    assert result ==[] #Для пустой коллекции ожидался пустой результат






transactions_data =[
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9824.07",
            "currency": {"name": "USD", "code": "USD"}
        }
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {
            "amount": "79114.93",
            "currency": {"name": "USD", "code": "USD"}
        }
    },
    {
        "id": 873106923,
        "state": "EXECUTED",
        "date": "2020-01-01",
        "operationAmount": {
            "amount": "1000",
            "currency": {"name": "RUB", "code": "RUB"}
        }
    },
    {
        "id": 594226727,
        "state": "EXECUTED",
        "date": "2020-02-02",
        "operationAmount": {
            "amount": "2000",
            "currency": {"name": "RUB", "code": "RUB"}
        }
    }
]