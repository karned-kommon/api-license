from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

class PayementStatus(str, Enum):
    UNPAID = "unpaid"
    OVERDUE = "overdue"
    PAID = "paid"
    CANCELLED = "cancelled"

class SalesModel(BaseModel):
    uuid: str = Field(..., description='UUID de la vente')
    date: datetime = Field(..., description='Date de la vente au format ISO 8601')
    status: PayementStatus = Field(PayementStatus.UNPAID, description='Status de la vente')