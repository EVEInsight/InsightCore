from InsightCore.models.BaseModel import BaseModel
from dataclasses import dataclass


@dataclass
class SystemRangeGate(BaseModel):
    system_id: int
    range: int


@dataclass
class SystemRangeLightyear(BaseModel):
    system_id: int
    range: float
