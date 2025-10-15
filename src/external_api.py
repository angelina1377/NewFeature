import os
from typing import Dict, Optional

import requests

API_KEY = os.getenv("API_KEY")
API_URL = "https://api.apilayer.com/exchangerates_data/convert"
TIMEOUT_SECONDS = 10


def convert_to_rub(from_currency: str, amount: float, date: Optional[str] = None) -> float:
    if from_currency.upper() == "RUB":
        return float(amount)

    if from_currency.upper() not in ("USD", "EUR"):
        raise ValueError(f"Unsupported currency for conversion: {from_currency}")

    if not API_KEY:
        raise RuntimeError("API key not set in environment variable API_KEY")

    params = {"from": from_currency.upper(), "to": "RUB", "amount": amount}
    if date:
        params["date"] = date

    headers = {"apikey": API_KEY}

    try:
        resp = requests.get(API_URL, params=params, headers=headers, timeout=TIMEOUT_SECONDS)
    except requests.RequestException as exc:
        raise RuntimeError(f"Network error while calling exchange API: {exc}") from exc

    if resp.status_code != 200:
        raise RuntimeError(f"Exchange API returned status {resp.status_code}: {resp.text}")

    try:
        data = resp.json()
    except ValueError as exc:
        raise RuntimeError("Invalid JSON from exchange API") from exc

    if "result" not in data:
        raise RuntimeError("No result field in exchange API response")

    try:
        return float(data["result"])
    except (TypeError, ValueError) as exc:
        raise RuntimeError("Invalid result value from exchange API") from exc


def transaction_amount_in_rub(transaction: Dict) -> float:
    if not isinstance(transaction, dict):
        raise TypeError("transaction must be a dict")

    amount_raw = None
    currency_raw = None

    op = transaction.get("operationAmount")
    if isinstance(op, dict):
        amount_raw = op.get("amount")
        cur = op.get("currency")
        if isinstance(cur, dict):
            currency_raw = cur.get("code")

    if amount_raw is None:
        amount_raw = transaction.get("amount")
    if currency_raw is None:
        currency_raw = transaction.get("currency")

    date_str = transaction.get("date") or transaction.get("data")

    if amount_raw is None or currency_raw is None:
        raise KeyError("Transaction missing amount or currency fields")

    # Простая проверка и преобразование в float
    try:
        amount_float = float(amount_raw)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid amount value: {amount_raw}") from exc

    currency_code = str(currency_raw).upper()

    if currency_code == "RUB":
        return amount_float

    if currency_code not in ("USD", "EUR"):
        raise ValueError(f"Unsupported currency: {currency_code}")

    result = convert_to_rub(currency_code, amount_float, date=date_str)
    return float(result)


if __name__ == "__main__":
    tx_example = {"operationAmount": {"amount": "12.34", "currency": {"code": "USD"}}, "date": "2024-01-01"}
    try:
        print("Сумма в RUB:", transaction_amount_in_rub(tx_example))
    except Exception as e:
        print("Ошибка:", e)