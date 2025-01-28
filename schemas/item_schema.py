
def item_serial(item) -> dict:
    return {
        "uuid": str(item["_id"]),
        "username": item["username"],
        "firstname": item.get("firstname"),
        "lastname": item.get("lastname"),
        "email": item.get("email"),
        "created_by": item.get("created_by")
    }


def list_item_serial(items) -> list:
    return [item_serial(item) for item in items]
