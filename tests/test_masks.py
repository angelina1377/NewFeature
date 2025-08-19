import pytest

from src.masks import get_mask_card_number, get_mask_account


def test_get_mask_card_number() -> None:
    """
    Функция тестирования масок карт
    :return: None
    """
    assert get_mask_card_number("2154122142121252") == "2154 12** **** 1252"
    with pytest.raises(ValueError):
        get_mask_card_number("21541221421212")

    with pytest.raises(ValueError):
        get_mask_card_number("")


def test_get_mask_account() -> None:
    """
    Функция тестирования номеров счета
    :return: None
    """
    assert get_mask_account("98665487554121452312") == "**2312"
    with pytest.raises(ValueError):
        get_mask_account("1154122")

    with pytest.raises(ValueError):
        get_mask_account("")