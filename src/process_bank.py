import re
from collections import Counter

def process_bank_search(transactions:list[dict], search_pattern:str)->list[dict]:
    # Функция поиска банковских операций по регулярному выражению
    pattern = re.compile(search_pattern, re.IGNORECASE)
    # Компиляция регулярное выражение с флагом IGNORECASE
    return [tx for tx in transactions if pattern.search(tx.get("description", ""))]
    # Фильтрация транзакций

def process_bank_operations(data:list[dict], categories:list)->dict:
    # Функция подсчета количества операций по категориям
    # data - список словарей с операциями
    # categories список категорий для подсчета
    # Проверка типа данных
    if not isinstance(data, list):
        raise TypeError("Данные должны быть списком")
    # Проверка типа категорий
    if not isinstance(categories, list):
        raise TypeError("Категории должны быть списком")
    # Проверка элементов списка
    for item in data:
        if not isinstance(item, dict):
            raise TypeError("Элементы данных должны быть словарями")
        if "description" not in item:
            raise TypeError ("Каждый словарь должен содержать ключ 'description'")
        if item["description"] is None:
            raise TypeError("Значение 'description' не может быть None")

    descriptions =  [operation["description"] for operation in data
                         if operation["description"] in categories]
    # Извлекаем описания операций, которые есть в категориях
    counter = Counter(descriptions)
    # Подсчитываем кол-во операций
    result = {}
    # Создаем пустой словарь
    for category in categories:
        # Проходим по каждой категории в списке categories
        # Проверяем есть ли эта категория в counter
        # Если категория есть в counter, берем ее значение
        # Если нет - ставим 0

        result[category] = counter.get(category, 0)

    return result



    # Тестовые данные
#test_transactions = [
 #   {
 #       "description": "Перевод на счет 4081781000000000001",
 #       "amount": 1000
 #   },
 #  {
 #      "description": "Оплата в магазине Пятерочка",
 #       "amount": 500
  #  },
  #  {
  #      "description": "Снятие наличных в банкомате",
   #     "amount": 2000
  #  }
#]
# Пример использования
#if __name__ == "__main__":
 #   result = process_bank_search(test_transactions, "оплата")
 #   print(result)