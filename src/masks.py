def get_mask_card_number(card_number: str) -> str:
    """Функция маскировки номера банковской карты"""
    if not card_number.isdigit() or len(card_number) != 16:
        raise ValueError("Номер карты должен состоять из 16 цифр.")
    """Проверка карты на длину и что она состоит из цифр"""

    first_part = card_number[:6]
    last_part = card_number[-4:]
    """Разбиваем номер карты на части"""

    masked_card_number: str = f"{first_part[:4]} {first_part[4:]}** **** {last_part}"

    return masked_card_number


def get_mask_account(account_number: str) -> str:
    """Функция маскировки номера банковского счета"""
    if not account_number.isdigit() or len(account_number) != 20:
        raise ValueError("Номер счета должен состоять из 20 цифр.")
    """Проверка счета на длину и что он состоит из цифр"""

    masked_part = "**"
    last_part = account_number[-4:]
    """Разбиваем номер счета на части"""

    masked_account_number: str = f"{masked_part}{last_part}"

    return masked_account_number
