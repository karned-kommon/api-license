import logging
from datetime import datetime


def sales_serial(item) -> dict:
    return {
        "uuid": str(item["uuid"]),
        "iat": int(item["iat"]),
        "status": str(item["status"])
    }


def list_sales_serial(items) -> list:
    return [sales_serial(item) for item in items]
