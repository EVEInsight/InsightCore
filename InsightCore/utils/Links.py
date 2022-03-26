class Links(object):
    @classmethod
    def type_image_64(cls, type_id: int):
        return f"https://image.eveonline.com/Type/{type_id}_64.png"

    @classmethod
    def faction_logo_64(cls, faction_id: int):
        return f"https://images.evetech.net/corporations/{faction_id}/logo?size=64"

    @classmethod
    def alliance_logo_64(cls, alliance_id: int):
        return f"https://images.evetech.net/alliances/{alliance_id}/logo?size=64"

    @classmethod
    def corporation_logo_64(cls, corporation_id: int):
        return f"https://images.evetech.net/corporations/{corporation_id}/logo?size=64"

    @classmethod
    def mail_zk_url(cls, mail_id: int):
        return f"https://zkillboard.com/kill/{mail_id}/"

    @classmethod
    def zk_character_url(cls, character_id: int):
        return f"https://zkillboard.com/character/{character_id}/"

