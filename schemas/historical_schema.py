def historical_serial(item) -> dict:
    return {
        "iat": int(item["iat"]),
        "exp": int(item["exp"]),
        "user_uuid": str(item["user_uuid"])
    }


def list_historical_serial(items) -> list:
    return [historical_serial(item) for item in items]