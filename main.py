import os
from typing import Dict, List, Tuple, Any
from src.processing import filter_by_state, sort_by_date
from src.widget import mask_account_card, get_date
from src.generators import filter_by_currency
from src.utils import load_operations
from src.finance import read_finance_csv_operation, read_finance_excel_operation
from src.process_bank import process_bank_search


# Определяем корневую директорию проекта (где лежит этот файл)
ROOT_DIR = os.path.dirname(__file__)

# Словарь действий пользователя: номер -> (описание, путь к данным)
# Словарь-где ключ- номер пункта меню
# Значения- кортеж и описанием и путем транзакции
func_answer: Dict[int, Tuple[str, str]] = {
    1: ("Получить информацию о транзакциях из JSON-файла", f"{ROOT_DIR}/data/operations.json"),
    2: ("Получить информацию о транзакциях из CSV-файла", f"{ROOT_DIR}/data/transactions.csv"),
    3: ("Получить информацию о транзакциях из XLSX-файла", f"{ROOT_DIR}/data/transactions_excel.xlsx"),
}

def get_user_menu() -> int:
    """
    Выводит меню и возвращает выбор пользователя как целое число.
    """
    for answer in sorted(func_answer.keys()):
        print(f"{answer}. {func_answer[answer][0]}")
    # считываем ввод пользователя и приводим к целому числу
    user_menu_input = input().strip()
    # выводим выбранное описание для подтверждения
    print(f"{func_answer[int(user_menu_input)][0]}")
    return int(user_menu_input)

# Возможные статусы транзакций
status: List[str] = ["EXECUTED", "CANCELED", "PENDING"]

def get_user_status() -> str:
    """
    Просит у пользователя статус для фильтрации и возвращает валидный статус.
    """
    while True:
        print(f"Доступные для фильтровки статусы: {', '.join(status)}")
        input_data = input().strip()
        upper_filter_user = input_data.upper()

        if upper_filter_user not in status:
            print(f'Статус операции "{input_data}" недоступен.')
            print("Введите статус, по которому необходимо выполнить фильтрацию.")
        else:
            print(f'Операции отфильтрованы по статусу "{upper_filter_user}"')
            return upper_filter_user

# Сопоставление ответов да/нет
answer_yes_no: Dict[str, bool] = {"Да": True, "Нет": False}

def _normalize_yes_no(answer: str) -> str:
    """Вспомогательная функция для нормализации ввода: возвращает текст в нужном регистре."""
    return answer.strip()

def get_user_answer() -> bool:
    """
    Считывает ответ пользователя и возвращает булево значение.
    По умолчанию возвращает "Да", если ввод непонятен.
    """
    input_data = input().strip()
    key = input_data.title()
    if key in answer_yes_no:
        return answer_yes_no[key]
    return answer_yes_no["Да"]

# Соответствие между выбором сортировки и логическим значением reverse
sorted_min_max: Dict[str, bool] = {"по возрастанию": False, "по убыванию": True}

def get_user_min_max_sorted() -> bool:
    """
    Спрашивает способ сортировки и возвращает булево значение reverse.
    """
    input_data = input().strip()
    key = input_data.lower()
    if key in sorted_min_max:
        return sorted_min_max[key]
    return sorted_min_max["по возрастанию"]

# Меню операций: ключ -> функция чтения данных

menu: Dict[int, Any[..., List[dict]]] = {
    1: load_operations,
    2: read_finance_csv_operation,
    3: read_finance_excel_operation
}

def main() -> None:
    """
    Главная функция приложения:
    - выводит приветствие и меню
    - читает данные выбранного типа
    - применяет фильтры по статусу
    - по желанию сортирует по дате
    - фильтрует по валюте (рубли/доллары)
    - по желанию фильтрует по слову в описании
    - печатает итоговый список и вызывает отображение
    """
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню ниже:")
    num_menu = get_user_menu()

    # читаем данные по выбранному формату файла
    data_read_file = menu[num_menu](func_answer[num_menu][1])

    print("Введите статус, по которому необходимо выполнить фильтрацию.")
    state = get_user_status()
    current_data = filter_by_state(data_read_file, state=state)

    print("Отсортировать операции по дате? Да/Нет")
    sort_date = get_user_answer()
    if sort_date:
        print("Отсортировать по возрастанию или по убыванию?")
        sorted_min_max_value = get_user_min_max_sorted()
        current_data = sort_by_date(current_data, sort_reverse=sorted_min_max_value)

    print("Выводить только рублевые транзакции? Да/Нет")
    only_rub_transactions = get_user_answer()
    currency = "RUB" if only_rub_transactions else "USD"
    current_data = list(filter_by_currency(current_data, currency=currency))

    print("Отфильтровать список транзакций по определенному слову в описании? Да/Нет")
    filter_word = get_user_answer()
    if filter_word:
        find_word = input("Введите искомое слово\n").strip()
        current_data = process_bank_search(current_data, word=find_word)

    print("Распечатываю итоговый список транзакций...")
    print(f"Всего банковских операций в выборке: {len(current_data)}")

    result_main(current_data)

def result_main(current_data: List[Dict]) -> None:
    """
    Выводит отформатированную информацию по каждой транзакции.
    """
    for transaction in current_data:
        date = get_date(transaction["date"])
        # Получаем сумму; в разной схеме данных может быть: "amount" или в блоке operationAmount
        amount = transaction.get("amount", transaction.get("operationAmount", {}).get("amount"))
        from_transaction = mask_account_card(transaction["from"])
        to_transaction = mask_account_card(transaction["to"])
        description = transaction["description"]
        # Определяем валюту из разных полей данных
        currency_code = (
            transaction.get("currency_code",
                            transaction.get("operationAmount", {}).get("currency", {}).get("name"))
        )
        print(f"{date} {description}\n{from_transaction} -> {to_transaction}\nСумма: {amount} {currency_code}\n\n")

if __name__ == "__main__":
    main()