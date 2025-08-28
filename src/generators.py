from typing import (
    Any,
    Dict,
    Generator,
    Iterator,
    List
)

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


def transaction_descriptions(list_data: List[Dict[str, object]]) -> Generator[str, None, None]:
    """

    :param list_data: список словарей с транзакциями
    :return: генератор с описанием транзакции
    """

    if not isinstance(list_data, list):
        raise TypeError("Ожидается список транзакций")

    def generator():
        if len(list_data) == 0:
            raise ValueError("Список транзакий не должен быть пустым")
        for transaction in list_data:  # Перебираем каждую транзакцию в списке
            if not isinstance(transaction, dict):
                raise TypeError("Элемент списка не является словарем")

            yield transaction.get("description", "Описание отсутствует")
    return generator()



def card_number_generator(start: int, stop: int) -> list:
    """

    :param start:начальное значение
    :param stop:конечное значение
    :return:список номеров
    """

# Проверка типов входных данных
    if not isinstance(start, int):
        raise TypeError("start должен быть целым числом")
    if not isinstance(stop, int):
        raise TypeError("stop должен быть целым числом")

    # Проверяем корректность входных данных
    if not (1 <= start <= 9999999999999999):
        raise ValueError("Начальное значение должно быть от 1 до 9999999999999999 ")
    if not (1 <= stop <= 9999999999999999):
        raise ValueError("Конечное значение должно быть от 1 до 9999999999999999 ")
    if start > stop:
        raise ValueError("Начальное значение должно быть меньше или равно конечному ")

    result = []

    for i_range in range(start, stop + 1):  # Добавляем +1 для включения stop
        zfill_res = str(i_range).zfill(16)
        temp_data = []

        for i in range(0, len(zfill_res), 4):
            temp_data.append(zfill_res[i : i + 4])

        result.append(" ".join(temp_data))

    return result
