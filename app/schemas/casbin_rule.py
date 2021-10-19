from pydantic import BaseModel
from enum import Enum
from typing import Optional
from datetime import datetime


class PolicyTypeEnum(str, Enum):
    p = "p"
    g = "g"


class CasbinPolicy(BaseModel):
    ptype: PolicyTypeEnum
    v0: Optional[str]
    v1: Optional[str]
    v2: Optional[str]
    v3: Optional[str]
    v4: Optional[str]
    v5: Optional[str]
    created_at: datetime
    created_by: str

    class Config:
        orm_mode = True




    


