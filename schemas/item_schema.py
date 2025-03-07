import logging

from schemas.historical_schema import list_historical_serial
from schemas.sales_schema import list_sales_serial


def item_serial(item) -> dict:
    return {
        "uuid": str(item["_id"]),
        "type_uuid": str(item["type_uuid"]),
        "name": str(item["name"]),
        "auto_renew": bool(item["auto_renew"]),
        "iat": int(item["iat"]),
        "exp": int(item["exp"]),
        "user_uuid": str(item["user_uuid"]),
        "entity_uuid": str(item["entity_uuid"]),
        "credential_uuid": str(item["credential_uuid"]),
        "historical": list_historical_serial(item["historical"]),
        "sales": list_sales_serial(item["sales"])
    }


def list_item_serial(items) -> list:
    return [item_serial(item) for item in items]
