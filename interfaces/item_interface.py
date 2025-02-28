from abc import ABC, abstractmethod
from typing import List
from models.item_model import Item


class ItemRepository(ABC):

    @abstractmethod
    def create_item(self, item_create: Item):
        pass

    @abstractmethod
    def get_item(self, item_id: str):
        pass

    @abstractmethod
    def list_items(self, filters: dict):
        pass

    @abstractmethod
    def update_item(self, item_id: str, item_update: Item):
        pass

    @abstractmethod
    def delete_item(self, item_id: str):
        pass

    @abstractmethod
    def close(self):
        pass