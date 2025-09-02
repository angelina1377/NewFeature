import pytest
from _pytest.capture import CaptureFixture

from src.decorators import log


def test_decorator_capsys(capsys: CaptureFixture[str]) -> None:
    @log()
    def num_div(x: int, y: int) -> float:
        return x / y

    # успешный вызов - лог в консоль
    num_div(6, 2)

    # неуспешный вызов - исключение и лог об ошибке в консоль
    with pytest.raises(ZeroDivisionError):
        num_div(6, 0)

    # читаем вывод один раз
    captured = capsys.readouterr()

    # Проверяем, что лог успешного вызова есть
    assert "num_div ok" in captured.out

    # Проверяем, что лог ошибки есть
    assert "ZeroDivisionError" in captured.out or "ZeroDivisionError" in captured.err
