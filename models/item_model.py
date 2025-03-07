from typing import Optional, List
from pydantic import BaseModel, Field

from models.sales_model import SalesModel
from models.historical_model import HistoricalModel


class Item(BaseModel):
    uuid: str = Field(..., description="License : UUID")
    type_uuid: str = Field(..., description="Type : UUID")
    name: str = Field(..., description="License name")
    auto_renew: bool = Field(default=True, description="Auto renew")
    iat: int = Field(..., description="license iat")
    exp: int = Field(..., description="License exp")
    user_uuid: str = Field(..., description="User UUID")
    entity_uuid: str  = Field(..., description="Entity UUID")
    credential_uuid: str = Field(..., description="Credential UUID")
    historical: List[HistoricalModel] = Field(..., description="License assignment historical data")
    sales: List[SalesModel] = Field(..., description="License sales data")









