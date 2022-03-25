from InsightCore.models.BaseModel import BaseModel
from dataclasses import dataclass


@dataclass
class Post(BaseModel):
    url: str
    visual_type: str  # post type one of: discord
    running: bool = True
    visual_id: int = 1


@dataclass
class DiscordPost(Post):
    visual_type: str = "discord"
    color_kill: int = 16711680
    color_loss: int = 65299
    color_time_60s: int = 12124259
    color_time_300s: int = 8454210
    color_time_else: int = 4128800
    color_generic: int = 2640791
