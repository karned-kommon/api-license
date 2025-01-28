from typing import Optional
from pydantic import BaseModel, Field, field_validator, EmailStr

class Item(BaseModel):
    uuid: str = Field(..., description="User : UUID")
    username: str = Field(..., description="User : username")
    firstname: Optional[str] = Field(None, description="User : firstname")
    lastname: Optional[str] = Field(None, description="User : lastname")
    email: EmailStr = Field(..., description="User : email")
    created_by: Optional[str] = Field(None, description="User who created this step")

    @field_validator("lastname", mode="before")
    def lastname_to_upper( cls, v ):
        return v.upper() if v else None

    @field_validator("firstname", mode="before")
    def firstname_to_capitalize( cls, v ):
        return v.capitalize() if v else None

    @field_validator("email", mode="before")
    def email_to_lower( cls, v ):
        return v.lower() if v else None

    @field_validator("username", mode="before")
    def username_to_lower( cls, v ):
        return v.lower() if v else None


