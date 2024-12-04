from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class TargetCreateScheme(BaseModel):
    name: str
    country: str


class TargetGetScheme(BaseModel):
    id: int
    name: str
    country: str
    is_completed: bool

    model_config = ConfigDict(from_attributes=True)


class MissionCreateScheme(BaseModel):
    spy_cat_id: Optional[int]
    targets: List[TargetCreateScheme]


class MissionGetScheme(BaseModel):
    id: int
    spy_cat_id: int
    targets: List[TargetGetScheme]

    model_config = ConfigDict(from_attributes=True)
