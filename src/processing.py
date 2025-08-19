def filter_by_state(data: list[dict], state: str ="EXECUTED") -> list[dict]:  # Функция нового списка
    """

    :param data: Список словарей
    :param state:  Значение для ключа
    :return: Список словарей отсортированные по ключу
    """
    return [item for item in data if item.get("state") == state]


def sort_by_date(operations: list[dict], reverse: bool = True) -> list[dict] :#Сортировка списка по дате
    """

    :param operations: Список словарей
    :param reverse: Порядок сортировки
    :return: Возврат отсортированного листа со списком
    """
    return sorted(operations, key=lambda x:x["date"], reverse=reverse)

transactions = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
]

# Сортировка по убыванию
sorted_desc = sort_by_date(transactions)
print(sorted_desc)

# Сортировка по возрастанию
sorted_asc = sort_by_date(transactions, reverse=False)
print(sorted_asc)
