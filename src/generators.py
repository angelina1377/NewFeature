from typing import List, Dict, Iterator, Any, Generator

# типы для более точной типизации, так как mypy никак не хочет принимать мою работу
Transaction = Dict[str, Any]
CurrencyInfo = Dict[str, str]
OperationAmount = Dict[str, Any]


def filter_by_currency(transactions: List[Transaction], currency_code: str) -> Iterator[Transaction]:
    """
    Функция, принимающая транзакции на вход
        :param transaction: список транзакций
        :param currency_code: код валюта операции
        :return: итератор транзакций с указанной валютой
    """
    for tx in transactions:  # Проходим по каждой транзакции в списке
        # Обрабатываем вложенную структуру operationAmount
        operation_amount: OperationAmount = tx.get("operationAmount", {})
        currency_info: CurrencyInfo = operation_amount.get("currency", {})
        code_op = currency_info.get("code")

        # Если код валюты совпадает с указанным или код валюты в operationAmount совпадает
        if str(code_op) == currency_code:
            yield tx  # Возвращаем транзакцию через итератор

def transaction_descriptions(list_data: list[dict]) -> Generator:
    """

    :param list_data: список словарей
    :return: генератор с описанием транзакции
    """
    if not list_data:#Проверка на пустой список
        raise ValueError("Список транзакций не должен быть пустым")#Выбрасывается исключение

    for transaction in list_data:#Перебираем каждую транзакцию в списке
        try:
            yield  transaction["description"]#Пытаемся получить описание транзакции
        except KeyError:#Если ключа "description" нет в словаре
            yield "Описание отсутствует"#Возвращается сообщение
