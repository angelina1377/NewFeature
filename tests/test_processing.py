import pytest

from src.processing import filter_by_state, sort_by_date

@pytest.fixture
def x_data():
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2023-01-01"},
        {"id": 594226727, "state": "CANCELED", "date": "2023-02-01"},
        {"id": 615064591, "state": "CANCELED", "date": "2023-03-01"},
        {"id": 939719570, "state": "EXECUTED", "date": "2023-04-01"}
    ]

@pytest.mark.parametrize(
    "state, result",
    [("EXECUTED", [41428829, 939719570]),
     ("CANCELED", [594226727, 615064591]),
     ("", [])
     ]

)
def test_filter_by_state(x_data: list[dict], state: str, result: list[int]) -> None:
    """

    :param x_data: Тестовые данные
    :param state: Аргумент фильтра значения
    :param result: Данные с параметризации
    :return:  None
    """
    filtered_data = filter_by_state(x_data, state=state)
    actual_ids = [item["id"] for item in filtered_data]
    assert sorted (actual_ids) == sorted(result)#Сортировка для корректного сравнения


def test_sort_by_date(x_data: list[dict]) -> None:  #"Функция сортировки данных по дате"
    sort_data: list[dict] = sort_by_date(x_data)
    false_reverse_data = sort_by_date(x_data, reverse=False)

    list_actual_ids = [item['id'] for item in sort_data]
    list_false_actual_ids = [item['id'] for item in false_reverse_data]

    assert list_actual_ids == [939719570, 615064591, 594226727, 41428829]
    assert list_false_actual_ids == [41428829, 594226727, 615064591, 939719570]
