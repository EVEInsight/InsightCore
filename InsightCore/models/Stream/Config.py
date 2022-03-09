from dataclasses import dataclass, asdict
from InsightCore.models.BaseModel import BaseModel


@dataclass
class Config(BaseModel):
    running: bool = True

