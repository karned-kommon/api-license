from pydantic import BaseModel, Field

class HistoricalModel(BaseModel):
    iat: int = Field(..., description="IAT")
    exp: int = Field(..., description="Exp")
    user_uuid: str = Field(..., description="User UUID")
