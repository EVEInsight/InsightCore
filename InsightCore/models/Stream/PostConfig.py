from InsightCore.models.BaseModel import BaseModel
from dataclasses import dataclass


@dataclass
class PostConfig(BaseModel):
    url: str
    link_only: bool = True
    running: bool = True


@dataclass
class DiscordPostConfig(PostConfig):
    color_kill: int = 16711680
    color_loss: int = 65299
    color_time_60s: int = 12124259
    color_time_300s: int = 8454210
    color_time_else: int = 4128800
    color_generic: int = 2640791
    link_only: bool = False
