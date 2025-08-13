from src.masks import get_mask_card_number, get_mask_account
def mask_account_card(info_number: str) -> str:
    """Функция,которая обрабатывает информацию как о картах, так и о счетах"""
    list_alpha = []
    list_digit = []
    parts = info_number.split()  # Удаляем лишние  пробелы

    for part in parts:
        if part.isalpha():
            list_alpha.append(part)  # Проверка наличия слов
        else:
            list_digit.append(part)  # Добавляем оставшуюся часть
    result = "".join(list_digit)  # Делаем строку
    masked_number = ""

    if len(result) == 16:
        masked_number = get_mask_card_number(result)

    elif len(result) == 20:
        masked_number = get_mask_account(result)
    else:
        raise ValueError("Неизвестный тип информации")

    return f"{' '.join(list_alpha)} {masked_number}"  # Применяем необходимую маскировку


def get_date(y: str) -> str:
    """Функция по изменению формата строки даты"""
    year = y[0:4]  # Срез для года
    month = y[5:7]  # Срез для месяца
    day = y[8:10]  # Срез для дня

    formatted_date = f"{day}.{month}.{year}"
    return formatted_date