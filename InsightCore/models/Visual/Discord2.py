from dataclasses import dataclass
from .BaseDiscord import BaseDiscordEmbedEntity


@dataclass
class Discord2(BaseDiscordEmbedEntity):
    @classmethod
    def get_visual_id(cls):
        return 2

    def generate_payload(self):
        super().generate_payload()
        m = self.mail
        self.embed["author"] = {
            "name": "Kill" if not self.is_loss else "Loss",
            "url": m.zk_url,
        }
        if m.victim.affiliation_logo:
            self.embed["author"]["icon_url"] = m.victim.affiliation_logo

        self.embed["title"] = f"{m.victim.ship_type_name} destroyed in {m.system_name}({m.region_name})"
        v = m.victim
        fb = m.final_blow_attacker
        if m.involved == 1:
            involved_string = "solo"
        elif m.involved == 2:
            involved_string = "and **1** other"
        else:
            involved_string = f"and **{m.involved}** others"
        self.embed["description"] = f"**[{v.character_name}]({v.character_zk_url})({v.affiliation_name})** " \
                                    f"lost their **{v.ship_type_name}** to " \
                                    f"**[{fb.character_name}]({fb.character_zk_url})({fb.affiliation_name})** " \
                                    f"flying in a **{fb.ship_type_name}** {involved_string}."


