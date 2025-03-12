from pydantic import BaseModel


class LicenseUUID(BaseModel):
    uuid: str