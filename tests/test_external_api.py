from unittest.mock import Mock, patch

import pytest

import src.external_api as external_api


def make_resp(status=200, json_data=None, text=""):
    """Утилита: создаёт объект-ответ, похожий на requests.Response."""
    mock_resp = Mock()
    mock_resp.status_code = status
    mock_resp.text = text
    # resp.json() либо возвращает значение, либо бросает ValueError
    if isinstance(json_data, Exception):
        mock_resp.json.side_effect = json_data
    else:
        mock_resp.json.return_value = json_data
    return mock_resp


@patch("src.external_api.requests.get")
def test_convert_to_rub_success(mock_get):
    # Подставим корректный ответ от API
    mock_get.return_value = make_resp(json_data={"result": 123.45})
    with patch.object(external_api, "API_KEY", "dummy_key"):
        res = external_api.convert_to_rub("USD", 10.0)
    assert isinstance(res, float)
    assert res == 123.45


@patch("src.external_api.requests.get")
def test_convert_to_rub_with_date_param(mock_get):
    mock_get.return_value = make_resp(json_data={"result": 50})
    with patch.object(external_api, "API_KEY", "k"):
        res = external_api.convert_to_rub("EUR", 5.0, date="2024-01-01")
    # Проверяем, что requests.get вызван и в параметрах есть date
    assert mock_get.called
    _, kwargs = mock_get.call_args
    assert "params" in kwargs
    assert kwargs["params"]["date"] == "2024-01-01"
    assert res == 50.0


def test_convert_to_rub_no_api_key_raises():
    # Гарантируем, что API_KEY пустой
    with patch.object(external_api, "API_KEY", None):
        with pytest.raises(RuntimeError, match="API key not set"):
            external_api.convert_to_rub("USD", 1.0)


def test_convert_to_rub_unsupported_currency():
    with patch.object(external_api, "API_KEY", "k"):
        with pytest.raises(ValueError, match="Unsupported currency"):
            external_api.convert_to_rub("GBP", 1.0)


@patch("src.external_api.requests.get")
def test_convert_to_rub_http_error(mock_get):
    mock_get.return_value = make_resp(status=500, text="server error")
    with patch.object(external_api, "API_KEY", "k"):
        with pytest.raises(RuntimeError, match="Exchange API returned status 500"):
            external_api.convert_to_rub("USD", 1.0)


@patch("src.external_api.requests.get")
def test_convert_to_rub_invalid_json(mock_get):
    # resp.json() бросает ValueError
    mock_get.return_value = make_resp(json_data=ValueError("bad json"))
    with patch.object(external_api, "API_KEY", "k"):
        with pytest.raises(RuntimeError, match="Invalid JSON"):
            external_api.convert_to_rub("USD", 1.0)


@patch("src.external_api.requests.get")
def test_convert_to_rub_no_result_field(mock_get):
    mock_get.return_value = make_resp(json_data={"not_result": 1})
    with patch.object(external_api, "API_KEY", "k"):
        with pytest.raises(RuntimeError, match="No result field"):
            external_api.convert_to_rub("USD", 1.0)


@patch("src.external_api.requests.get")
def test_convert_to_rub_invalid_result_value(mock_get):
    mock_get.return_value = make_resp(json_data={"result": "not-a-number"})
    with patch.object(external_api, "API_KEY", "k"):
        with pytest.raises(RuntimeError, match="Invalid result value"):
            external_api.convert_to_rub("USD", 1.0)


@patch("src.external_api.requests.get")
def test_transaction_amount_in_rub_with_operationAmount_calls_api(mock_get):
    # Возвращаем 100 RUB в ответ на вызов API
    mock_get.return_value = make_resp(json_data={"result": 100.0})
    with patch.object(external_api, "API_KEY", "k"):
        tx = {"operationAmount": {"amount": "10.0", "currency": {"code": "USD"}}, "date": "2024-01-01"}
        res = external_api.transaction_amount_in_rub(tx)
    assert res == 100.0
    assert mock_get.called  # убедимся, что внешний вызов сделан


def test_transaction_amount_in_rub_rub_no_api_call():
    # Для RUB вызов convert_to_rub не должен обращаться к requests.get
    with patch("src.external_api.requests.get") as mock_get:
        tx = {"operationAmount": {"amount": "42.5", "currency": {"code": "RUB"}}}
        res = external_api.transaction_amount_in_rub(tx)
    assert res == 42.5
    mock_get.assert_not_called()


def test_transaction_missing_fields():
    with pytest.raises(KeyError):
        external_api.transaction_amount_in_rub({})


def test_transaction_invalid_amount_value():
    tx = {"amount": "not-a-number", "currency": "USD"}
    with pytest.raises(ValueError, match="Invalid amount value"):
        external_api.transaction_amount_in_rub(tx)
