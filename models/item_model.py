from typing import Optional, List
from pydantic import BaseModel, Field

from models.sales_model import SalesModel
from models.historical_model import HistoricalModel


class Item(BaseModel):
    uuid: str = Field(..., description="License : UUID")
    type_uuid: str = Field(..., description="Type : UUID")
    created_by: str = Field(..., description="Admin who created")
    sales: List[SalesModel] = Field(..., description="License sales data")
    name: str = Field(..., description="License name")
    iat: int = Field(..., description="license iat")
    exp: int = Field(..., description="License exp")
    user_uuid: str = Field(..., description="User UUID")
    manager_uuid: str = Field(..., description="Manager UUID")
    historical: List[HistoricalModel] = Field(..., description="License assignment historical data")
    auto_renew: bool = Field(default=True, description="Auto renew")
    credential_uuid: str = Field(..., description="Credential UUID")
    entity_uuid: str  = Field(..., description="Entity UUID")









