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
    iat: int = Field(..., description="IAT")
    status: PayementStatus = Field(PayementStatus.UNPAID, description='Status de la vente')