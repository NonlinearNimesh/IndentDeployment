from typing import Optional
from pydantic import BaseModel
from datetime import datetime, time
from datetime import datetime, time, timedelta

class DetailsBase(BaseModel):
    name: str
    username: str
    password: str
    email: str
    role: str
    secret_key: str
    key_expires: str
    created_on: str

class Detail(DetailsBase):
    id: int

    class Config:
        orm_mode = True