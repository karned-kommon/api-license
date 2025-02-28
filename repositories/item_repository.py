import logging
import json
from typing import List
from uuid import uuid4
from pymongo import MongoClient
from interfaces.item_interface import ItemRepository
from models.item_model import Item
from schemas.item_schema import list_item_serial, item_serial


class ItemRepositoryMongo(ItemRepository):

    def __init__( self, url: str, name: str, collection: str ):
        self.url = url
        self.name = name
        self.collection = collection
        self.client = None
        self.db = None

    def __enter__( self ):
        self.client = MongoClient(self.url)
        self.db = self.client[self.name]
        return self

    def __exit__( self, exc_type, exc_val, exc_tb ):
        self.client.close()

    def create_item(self, item_create: Item) -> str:
        item_data = item_create.model_dump()
        item_data["_id"] = str(item_data['uuid'])
        del(item_data['uuid'])
        new_uuid = self.db[self.collection].insert_one(item_data)
        return new_uuid.inserted_id

    def get_item(self, uuid: str) -> dict:
        result = self.db[self.collection].find_one({"_id": uuid})
        if result is None:
            return None
        else:
            item = item_serial(result)
            return item

    def list_items(self, filters: dict) -> List[dict]:
        query = filters
        result = self.db[self.collection].find(query)
        items = list_item_serial(result)
        return items

    def update_item(self, uuid: str, item_update: Item) -> None:
        update_data = {"$set": item_update.model_dump()}
        self.db[self.collection].find_one_and_update({"_id": uuid}, update_data)

    def delete_item(self, uuid: str) -> None:
        self.db[self.collection].delete_one({"_id": uuid})

    def close(self):
        self.client.close()