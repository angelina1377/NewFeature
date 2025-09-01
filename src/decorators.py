from functools import wraps


def log(filename=None):
    """ Декоратор для логирования вызовов функции
        Если указан filename, лог будет записываться в файл.
        Иначе -выводиться в консоль
    """
    def decorator(func):
        """ Внутренний декоратор, который оборачивает исходную функцию"""
        @wraps(func)
        def wrapper(*args, **kwargs):  # Обертка
            print(f"Начало выполнения функции'{func.__name__}' с аргументами args={args}, kwargs={kwargs}")

            try:
                # Вызываем исходную функцию с переданными аргументами
                result = func(*args, **kwargs)
                # Логируем успешное завершение функции и результат
                print(f"Функция '{func.__name__}' успешно завершилась с результатом: {result}")
                return result
            except Exception as e:
                # В случае ошибки логируем тип ошибки и сообщение
                error_type = type(e).__name__   # Получаем название типа исключения
                print(f"Ошибка в функции'{func.__name__}' : {error_type}."
                      f"Входные параметры args={args}, kwargs={kwargs}")
                print(f"Сообщение об ошибке: {e}")
                # После логирования ошибка пробрасывается дальше
                raise
        return wrapper
    return decorator


@log(filename="mylog.txt")
def my_function(x, y):
    return x + y


my_function(1, 2)
