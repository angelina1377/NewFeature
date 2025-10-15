import os
from typing import Dict, List, Tuple, Callable
from src.processing import filter_by_state, sort_by_date
from src.widget import mask_account_card, get_date
from src.generators import filter_by_currency
from src.utils import load_operations
from src.finance import read_finance_csv_operation, read_finance_excel_operation
from src.process_bank import process_bank_search


# Определяем корневую директорию проекта (где лежит этот файл)
# file-переменная которая сохраняет путь к текущему исполняемому файлу Python
# os.path.dirname извлекает из этого пути только путь к директории (без имени файла)
# Результат сохраняется в константу ROOT_DIR
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
    # Перебираем отсртированные ключи словаря func_answer
    for answer in sorted(func_answer.keys()):
        # Выводим пункты меню: func_answer[answer]- получаем кортеж из словаря
        # [0] - берем первый элемент кортежа(описание пункта меню)
        print(f"{answer}. {func_answer[answer][0]}")
    # считываем ввод пользователя и приводим к целому числу
    # strip() убирает пробелы в начале и конце строки
    user_menu_input = input().strip()
    # выводим выбранное описание для подтверждения
    # преобразуем ввод в целое число
    # [0] снова используется для получения описания из кортежа
    print(f"{func_answer[int(user_menu_input)][0]}")
    # Возвращаем выбранный номер в виде целого числа
    return int(user_menu_input)

# Возможные статусы транзакций
status: List[str] = ["EXECUTED", "CANCELED", "PENDING"]

def get_user_status() -> str:
    """
    Просит у пользователя статус для фильтрации и возвращает валидный статус.
    """
    while True:# Бесконечный цикл, который будет работать, пока не получим корректный ввод
        # Выводим доступные статусы
        print(f"Доступные для фильтровки статусы: {', '.join(status)}")
        # join объединяет их в строку через запятую
        # Получаем ввод от пользователя
        input_data = input().strip()
        # Приводим ввод к верхнему регистру чтобы сделать проверку нечувствительной к регистру
        upper_filter_user = input_data.upper()
        # Проверяем,является ли введеный статус допустимым
        if upper_filter_user not in status:
            # Если статус недопустимый
            print(f'Статус операции "{input_data}" недоступен.')
            print("Введите статус, по которому необходимо выполнить фильтрацию.")
        else:
            # Если статус допустимый
            print(f'Операции отфильтрованы по статусу "{upper_filter_user}"')
            return upper_filter_user # Возвращаем корректный статус

# Сопоставление ответов да/нет(словарь, где ключи-варианты ответов
answer_yes_no: Dict[str, bool] = {"Да": True, "Нет": False}

def _normalize_yes_no(answer: str) -> str:
    """_ в начале имени функции- Вспомогательная функция для нормализации ввода:
    возвращает текст в нужном регистре."""
    return answer.strip()# strip удаляет пробелы по краям
                         # возвращает нормализованную строку

def get_user_answer() -> bool:
    """
    Считывает ответ пользователя и возвращает булево значение.
    По умолчанию возвращает "Да", если ввод непонятен.
    """
    input_data = input().strip()# считываем ввод и убираем пробелы
    key = input_data.title()# приводим к нужному формату
                            # делает первое слово с большой буквы
    if key in answer_yes_no:# проверяем сеть ли такой ключ в словаре
        return answer_yes_no[key]# возвращаем соответствующее булево значение
    return answer_yes_no["Да"]# если ключ не найден возвращаем значение по умолчанию(True)

# Соответствие между выбором сортировки и логическим значением reverse
# Словарь для сортировки: ключи-варианты ввода пользователя
#                         значения параметры сортировки False-по возрастанию True- по убыванию
sorted_min_max: Dict[str, bool] = {"по возрастанию": False, "по убыванию": True}

def get_user_min_max_sorted() -> bool:
    """
    Спрашивает у пользователя способ сортировки и возвращает булево значение reverse.
    """
    # Считываем ввод пользователя
    input_data = input().strip()
    # Приводим ввод к ижнему регистру для унификации
    key = input_data.lower()
    # Проверяем есть ли такой ключ в словаре sorted_min_max
    if key in sorted_min_max:
        #Если ключ найден возвращаем соответствующее значение
        return sorted_min_max[key]
    # Если ключ не найден, возвращаем значение по умолчанию
    return sorted_min_max["по возрастанию"]

# Меню операций: ключ -> функция чтения данных

# Этот словарь связывает номера меню с функциями чтения данных
# Callable- указывает что значение является вызываемым объектом(функцией)
# str предполагаемый аргумент функции
# List[dict] возвращает список словарей
menu: Dict[int, Callable[[str], List[dict]]] = {
    1: load_operations, # Функция для чтения JSON
    2: read_finance_csv_operation, # Функция для чтения CSV
    3: read_finance_excel_operation # Функция для чтения Excel
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
    num_menu = get_user_menu() # Получаем выбор пользователя

    # читаем данные по выбранному формату файла
    # menu[num_menu] получаем ф-ю из словаря menu по выбранному номеру меню
    # func_answer[num_menu][1] получаем путь к файлу из словаря func_answer
    data_read_file = menu[num_menu](func_answer[num_menu][1])

    print("Введите статус, по которому необходимо выполнить фильтрацию.")
    state = get_user_status() # получаем статус от пользователя
    current_data = filter_by_state(data_read_file, state=state)# применяем фильтрацию

    print("Отсортировать операции по дате? Да/Нет")
    sort_date = get_user_answer()# получаем ответ от пользователя
    if sort_date:
        print("Отсортировать по возрастанию или по убыванию?")
        sorted_min_max_value = get_user_min_max_sorted()# получаем направление сортировки
        # current_data - данные которые нужно отсортировать
        # current_data текущие отфильтрованные списко транзакций
        # reverse параметр определяющий порядок сортировки
        # sorted_min_max_value - результат работы ф-ции get_user_min_max_sorted()
        current_data = sort_by_date(current_data, reverse=sorted_min_max_value)

    print("Выводить только рублевые транзакции? Да/Нет")
    # ф-ция get_user_answer  возвращает True- Да False- Нет
    only_rub_transactions = get_user_answer()# получаем ответ пользователя
    currency = "RUB" if only_rub_transactions else "USD"# определяем валюту
    # фильтруем данные
    current_data = list(filter_by_currency(current_data, currency_code =currency))

    print("Отфильтровать список транзакций по определенному слову в описании? Да/Нет")
    filter_word = get_user_answer()# получаем ответ пользователя
    if filter_word:# если пользователь выбрал Да
        find_word = input("Введите искомое слово\n").strip()# запрашиваем слово для поиска
        current_data = process_bank_search(current_data, search_pattern=find_word)# фильтруем данные

    print("Распечатываю итоговый список транзакций...")
    print(f"Всего банковских операций в выборке: {len(current_data)}")# показываем кол-во оставшихся транзакций после всех фильтров

    result_main(current_data)# сюда передаем отфильтрованные данные


def result_main(current_data: List[Dict]) -> None:
    """
    Выводит отформатированную информацию по каждой транзакции.
    current_data список словарей с данными транзакций
    """
    for transaction in current_data: # перебираем каждую транзакцию
        date = get_date(transaction["date"])# получаем отформатированную дату
        # Получаем сумму; в разной схеме данных может быть: "amount" или в блоке operationAmount
        amount = transaction.get("amount", transaction.get("operationAmount", {}).get("amount"))
        # сначала ищет поле amount в корне
        # если не находит ищет внутри operationAmount
        # Маскируем данные отправителя и получателя
        from_transaction = mask_account_card(transaction["from"])
        to_transaction = mask_account_card(transaction["to"])
        description = transaction["description"]# получаем описание операции
        # Получаем код валюты с учетом разных структур данных
        currency_code = (
            transaction.get("currency_code",
                            transaction.get("operationAmount", {}).get("currency", {}).get("name"))

        )
        # сначала ищет currency_code в корне
        # если не находит ищет внутри
        # Выводим отформатированную информацию внутри operationAmount -> currency -> name
        # Дата+описаие+отправитель-> получатель+сумма+валюта
        print(f"{date} {description}\n{from_transaction} -> {to_transaction}\nСумма: {amount} {currency_code}\n\n")

if __name__ == "__main__":
    main()