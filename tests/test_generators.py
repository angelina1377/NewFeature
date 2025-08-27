import pytest

from src.generators import filter_by_currency, transaction_descriptions, card_number_generator

from typing import List, Dict, Generator, Union


Transaction = Dict[str, Union[str, int, float, Dict]]
CurrencyInfo = Dict[str, str]
OperationAmount = Dict[str, Union[str, float]]


@pytest.mark.parametrize(
    "currency, expected_ids",
    [
        ("USD", [939719570, 142264268]),
        ("RUB", [873106923, 594226727]),
        ("EUR", []),
        ("USD", [939719570, 142264268]),
        ("XYZ", []),
    ],
)
def test_filter_by_currency(currency: str, expected_ids: List[int]) -> None:  # Фильтрация
    # Получаем отфильтрованные транзакции
    filtered_transactions: List[Transaction] = list(filter_by_currency(transactions_data, currency))
    # Извлекаем id из полученных транзакций
    result_ids: List[int] = [tx["id"] for tx in filtered_transactions]
    # Проверяем соответствие
    assert result_ids == expected_ids, f"Неверный результат для валюты {currency}"

    # Дополнительный тест для пустой коллекции


def test_empty_transactions() -> None:
    empty_transactions: List[Transaction] = []
    result: List[Transaction] = list(filter_by_currency(empty_transactions, "USD"))
    assert result == []  # Для пустой коллекции ожидался пустой результат


transactions_data: List[Transaction] = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
    },
    {
        "id": 873106923,
        "state": "EXECUTED",
        "date": "2020-01-01",
        "operationAmount": {"amount": "1000", "currency": {"name": "RUB", "code": "RUB"}},
    },
    {
        "id": 594226727,
        "state": "EXECUTED",
        "date": "2020-02-02",
        "operationAmount": {"amount": "2000", "currency": {"name": "RUB", "code": "RUB"}},
    },
]


def test_transaction_descriptions() -> None:
    test_transactions: List[Dict[str, Union[str, int]]] = [
        {"description": "Перевод организации"},
        {"description": "Перевод со счета на счет"},
        {"description": "Перевод с карты на карту"},
        {"amount": 100},  # Транзакция без описания
    ]
    # Создаем генератор
    generator: Generator[str, None, None] = transaction_descriptions(
        test_transactions
    )  # Тест корректной работы с данными

    # Проверяем последовательность описаний
    assert next(generator) == "Перевод организации"
    assert next(generator) == "Перевод со счета на счет"
    assert next(generator) == "Перевод с карты на карту"
    assert next(generator) == "Описание отсутствует"

    # Проверка исчерпания генератора
    with pytest.raises(StopIteration):
        next(generator)

    # Проверка на None
    with pytest.raises(TypeError):
        transaction_descriptions(None)

    # Проверка на пустой список
    with pytest.raises(ValueError):
        next(transaction_descriptions([]))

    # Проверка на некорректный тип данных
    with pytest.raises(TypeError):
        transaction_descriptions("не список")


def test_empty_description() -> None:
    # Тест обработки отсутствующего ключа
    data = transaction_descriptions([{"amount": 100}])
    assert next(data) == "Описание отсутствует"


def test_card_number_generator() -> None:
    """

    :param start:начальное значение для генерации
    :param stop: конечное значение для генерации
    :param result: выдаваемое значение
    :return: None
    """
    assert card_number_generator(1234, 1234) == ["0000 0000 0000 1234"]
    assert card_number_generator(12345678, 12345678) == ["0000 0000 1234 5678"]

    expected = ["0000 0000 0000 1234", "0000 0000 0000 1235", "0000 0000 0000 1236"]
    assert card_number_generator(1234, 1236) == expected

    with pytest.raises(ValueError):
        card_number_generator(0, 0)

    with pytest.raises(ValueError):
        card_number_generator(10000000000000000, 10000000000000000)

    with pytest.raises(ValueError):
        card_number_generator(10, 5)

    with pytest.raises(TypeError):
        card_number_generator(None, 10)
