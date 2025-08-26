import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "data_number, result",
    [
        ("Visa Platinum 70007922548789606361", "Visa Platinum **6361"),
        ("Счет 7365410843014305", "Счет 7365 41** **** 4305"),
        ("MasterCard 71583007548734726758", "MasterCard **6758"),
    ],
)
def test_mask_account_card(data_number: str, result: str) -> None:
    """
    Функция проверки номеров карт
    :param data_number: Входные данные карт с параметризации
    :param result: Выходные данные карт с параметризации
    :return: None
    """
    assert mask_account_card(data_number) == result
    with pytest.raises(ValueError):
        mask_account_card("12125512")
    with pytest.raises(ValueError):
        mask_account_card("")


@pytest.mark.parametrize(
    "date, expected",
    [("2025-02-10", "10.02.2025"), ("2024-02-09", "09.02.2024"), ("2022-01-01", "01.01.2022")],
)
def test_get_date(date: str, expected: str) -> None:
    """
    Функция тестирования дат
    :param date: Входные данные дат с параметризации
    :param result: Выходные данные дат с параметризации
    :return: None
    """
    assert get_date(date) == expected
