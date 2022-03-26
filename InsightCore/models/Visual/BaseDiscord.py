from dataclasses import dataclass, field
from .BaseVisual import BaseVisual
from InsightCore.models.Stream import DiscordPost
from InsightCore.utils import Links, Formatters
from InsightCore.utils import Filters


@dataclass
class BaseDiscord(BaseVisual):
    @classmethod
    def get_visual_type(cls):
        return "discord"


@dataclass
class BaseDiscordEmbed(BaseDiscord):
    embed: dict = field(default_factory=dict)  # https://discord.com/developers/docs/resources/channel#embed-object

    def get_payload(self) -> dict:
        self.generate_payload()
        return {
            "embeds": [self.embed]
        }

    def generate_payload(self):
        self.embed["timestamp"] = self.mail.killmail_time.isoformat()
        if isinstance(self.stream.post, DiscordPost):
            self.embed["color"] = self.stream.post.color_generic


@dataclass
class BaseDiscordEmbedEntity(BaseDiscordEmbed):
    def wildcard_generic(self) -> bool:
        """Checks if all attacker related filters include wildcard.

        :return: True if all entity filters for attackers include wildcard, else False
        """
        if "*" in self.stream.filter.attacker_faction_ids_include and \
                "*" in self.stream.filter.attacker_alliance_ids_include and \
                "*" in self.stream.filter.attacker_corporation_ids_include and \
                "*" in self.stream.filter.attacker_character_ids_include:
            return True
        else:
            return False

    def generate_payload(self):
        super().generate_payload()
        self.embed["url"] = self.mail.zk_url
        if self.mail.victim.ship_type_id is not None:
            self.embed["thumbnail"] = {
                "url": Links.type_image_64(self.mail.victim.ship_type_id),
            }
        if self.mail.zkb_totalValue is not None:
            self.embed["footer"] = {
                "text": f"Value: {Formatters.short_str_isk(self.mail.zkb_totalValue)}"
            }

        if self.wildcard_generic():
            if isinstance(self.stream.post, DiscordPost):
                self.embed["color"] = self.stream.post.color_generic
        else:
            if isinstance(self.stream.post, DiscordPost):
                self.embed["color"] = self.stream.post.color_loss if self.is_loss else self.stream.post.color_kill
