import pytest
from src.process_bank import process_bank_search, process_bank_operations

@pytest.fixture
def sample_transactions():
    return  [
    {
        "description": "Перевод на счет 4081781000000000001",
        "amount": 1000
    },
    {
        "description": "Оплата в магазине Пятерочка",
        "amount": 500
    },
    {
        "description": "Снятие наличных в банкомате",
        "amount": 2000
    }
]

def test_process_bank_search(sample_transactions):
    result = process_bank_search(sample_transactions, "оплата")
    assert len(result) == 1
    assert result[0]["description"] == "Оплата в магазине Пятерочка"


# Тестовые данные
transactions = [
    {"description": "Перевод", "amount": 1000},
    {"description": "Оплата", "amount": 500},
    {"description": "Перевод", "amount": 2000},
    {"description": "Снятие", "amount": 1500},
    {"description": "Оплата", "amount": 300},
    {"description": "Другое", "amount": 100}
]

# Cоздаем тестовые данные- список транзакций
# Параметризация позволяет запустить несколько тестов с разными данными
# assert проверяет соответствие результата ожидаемому
# pytest.raises проверяет что функция генерирует правильные ошибки
@pytest.mark.parametrize("transactions,categories, expected", [
    # Тест 1: базовые категории
    (
            transactions,
            ["Перевод", "Оплата", "Снятие"],
            {"Перевод": 2, "Оплата": 2, "Снятие": 1}
    ),

    # Тест 2: категория, которой нет в данных
    (
            transactions,
            ["Перевод", "Оплата", "Пополнение"],
            {"Перевод": 2, "Оплата": 2, "Пополнение": 0}
    ),

    # Тест 3: пустая категория
    (
            transactions,
            [],
            {}
    ),

    # Тест 4: все категории присутствуют
    (
            transactions,
            ["Перевод", "Оплата", "Снятие", "Другое"],
            {"Перевод": 2, "Оплата": 2, "Снятие": 1, "Другое": 1}
    ),



    # Тест 5: отсутствующие
    (
            [
                {"description": "Перевод"},
                {"description": "Оплата"},
                {"description": "Перевод"}
            ],
            ["Перевод", "Оплата", "Снятие"],
            {"Перевод": 2, "Оплата": 1, "Снятие": 0}
    )
])
def test_process_bank_operations(transactions, categories, expected):# Функция теста с параметрами
    result = process_bank_operations(transactions, categories) # Вызываем тестируемую функцию
    assert result == expected # Проверяем,что результат совпадает с ожидаемым


def test_empty_transactions(): # Функция теста для пустого списка транзакций
    # Пустой список транзакций
    result = process_bank_operations([], ["Категория"])
    assert result == {"Категория": 0}


def test_invalid_data(): # Функция теста для проверки обработки ошибок
    # Невалидные данные
    with pytest.raises(TypeError):# В data есть словарь без ключа description
        process_bank_operations([{"amount": 100}], ["Категория"])

    with pytest.raises(TypeError): # Неверный тип (не список)
        process_bank_operations("не список", ["Категория"])

    with pytest.raises(TypeError): # В data есть словарь с description: None
        process_bank_operations([{"description": None}], ["Категория"])

    with pytest.raises(TypeError):# Неверный тип categories(не список)
        process_bank_operations([], "не список")

    with pytest.raises(TypeError):# В data есть элемент который не словарь
        process_bank_operations([123, {"description": "Перевод"}], ["Перевод"])

