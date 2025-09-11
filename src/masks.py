import logging
from datetime import datetime
from pathlib import Path

# Создаем директорию для логов, если её нет
PROJECT_ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = PROJECT_ROOT / "logs" # Создает новый путь, добавляя к корневой директории проекта папку logs
LOG_DIR.mkdir(parents=True, exist_ok=True) # не вызывает ошибку, если директория уже существует


def setup_logger():
    logger = logging.getLogger("bank_masking") # Создаем новый логгер с именем “bank_masking”
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    log_file = LOG_DIR / f'log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    # FileHandler — специальный обработчик для записи в фай
    # log_file — путь к файлу
    # mode="w" — режим записи (w — перезапись файла)
    # encoding="utf-8" — кодировка файла

    file_handler.setFormatter(formatter)

    if logger.handlers:
        logger.handlers.clear()
    logger.addHandler(file_handler)
    return logger
    # Проверяет, есть ли уже обработчики у логгера
    # Если есть — очищает их список
    # Добавляет новый обработчик (file_handler) к логгеру

logger = setup_logger()  # Инициализация логгера


def get_mask_card_number(card_number: str) -> str:
    try:
        # Проверка корректности номера карты
        if not card_number.isdigit() or len(card_number) != 16:
            raise ValueError("Номер карты должен состоять из 16 цифр.")
        # Логирование успешного прохождения валидации
        logger.info("Валидация номера карты прошла успешно")
        # Первая маскировка номера карты
        card_number = f"{card_number[:4]} {card_number[4:6]} ****** {card_number[-4:]}"
        logger.info(f"Номер карты успешно замаскирован: {card_number}")
        # Разделяе маскированный номер на части
        first_part = card_number[:6]
        last_part = card_number[-4:]
        # Вторая маскировка номера карты
        masked_card_number = f"{first_part[:4]} {first_part[4:]}** **** {last_part}"
        logger.info(f"Номер карты успешно замаскирован: {card_number}")
        return masked_card_number
        # logger.info записывает информацию

    except ValueError as e:
        # Логирование ошибки валидации
        logger.error(f"Ошибка валидации номера карты: {str(e)}")
        raise # исключение перебрасывается дальше


def get_mask_account(account_number: str) -> str:
    try:
        # Проверка корректности номера счета
        if not account_number.isdigit() or len(account_number) != 20:
            raise ValueError("Номер счета должен состоять из 20 цифр.")
        # Логгирование успешного прохождения валидации
        logger.info("Валидация номера счета прошла успешно")
        # Создание маскированной части
        masked_part = "**"
        # Получение последних 4 цифр счета
        last_part = account_number[-4:]
        # Формирование итогового замаскированного  номера
        account_number = f"{masked_part}{last_part}"
        # Логирование успешного маскирования
        logger.info(f"Номер счета успешно замаскирован: {account_number}")
        # Возврат результата
        return account_number

    except ValueError as e:
        logger.error(f"Ошибка валидации номера счета: {str(e)}")
        raise


if __name__ == "__main__":
    try:
        print(get_mask_card_number("1234567890123456"))
        print(get_mask_account("12345678901234567890"))

    except Exception as e:
        logger.critical(f"Критическая ошибка: {str(e)}")
