from dataclasses import dataclass, asdict
from core.models.BaseModel import BaseModel


@dataclass
class Config(BaseModel):
    running: bool = True

