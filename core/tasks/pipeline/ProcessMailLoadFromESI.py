from core.models.Mail.Mail import Mail, RedisQMail
from .EnqueueMailToStreams import EnqueueMailToStreams
from core.tasks.BaseTasks.InsightCoreTask import InsightCoreTask
from ESICelery.tasks.Alliance import *
from ESICelery.tasks.Character import *
from ESICelery.tasks.Corporation import *
from ESICelery.tasks.Market import *
from ESICelery.tasks.Universe import *


class ProcessMailLoadFromESI(InsightCoreTask):
    autoretry_for = (Exception,)
    max_retries = 25
    retry_backoff = 5
    retry_backoff_max = 600
    retry_jitter = False

    def run(self, mail_json) -> None:
        """Update mail object will all ESI resolved data.
        Raises NotResolved exceptions to trigger retries if the data hasn't been loaded from ESI yet.

        :param self: Celery self reference required for retries.
        :param mail_json: json dictionary containing RedisQ ZK data.
        :type mail_json: dict
        :raises core.exceptions.ESI.NotResolved: If the requested data has not yet been resolved by ESI.
        :rtype: None
        """
        m = Mail.from_json(RedisQMail.from_json(mail_json).to_json())

        if m.system_id:
            esi = SystemInfo().get_cached(system_id=m.system_id)
            m.system_name = esi
            m.system_security_status = esi
            m.system_pos_x = esi
            m.system_pos_y = esi
            m.system_pos_z = esi
            m.constellation_id = esi
            esi = ConstellationInfo().get_cached(constellation_id=m.constellation_id)
            m.constellation_name = esi
            m.region_id = esi
            esi = RegionInfo().get_cached(region_id=m.region_id)
            m.region_name = esi

        if m.victim:
            if m.victim.character_id:
                esi = CharacterPublicInfo().get_cached(character_id=m.victim.character_id)
                m.victim.character_name = esi
            if m.victim.corporation_id:
                esi = CorporationInfo().get_cached(corporation_id=m.victim.corporation_id)
                m.victim.corporation_name = esi
            if m.victim.alliance_id:
                esi = AllianceInfo().get_cached(alliance_id=m.victim.alliance_id)
                m.victim.alliance_name = esi
            if m.victim.faction_id:
                esi = FactionsList().get_cached()
                m.victim.faction_name = esi
            if m.victim.ship_type_id:
                esi = TypeInfo().get_cached(type_id=m.victim.ship_type_id)
                m.victim.ship_type_name = esi
                m.victim.ship_group_id = esi
                esi = GroupInfo().get_cached(group_id=m.victim.ship_group_id)
                m.victim.ship_group_name = esi
                m.victim.ship_category_id = esi
                esi = CategoryInfo().get_cached(category_id=m.victim.ship_category_id)
                m.victim.ship_category_name = esi
                esi = PricesList().get_cached()
                m.victim.ship_adjusted_price = esi

        for a in m.attackers:
            if a.character_id:
                esi = CharacterPublicInfo().get_cached(character_id=a.character_id)
                a.character_name = esi
            if a.corporation_id:
                esi = CorporationInfo().get_cached(corporation_id=a.corporation_id)
                a.corporation_name = esi
            if a.alliance_id:
                esi = AllianceInfo().get_cached(alliance_id=a.alliance_id)
                a.alliance_name = esi
            if a.faction_id:
                esi = FactionsList().get_cached()
                a.faction_name = esi
            if a.ship_type_id:
                esi = TypeInfo().get_cached(type_id=a.ship_type_id)
                a.ship_type_name = esi
                a.ship_group_id = esi
                esi = GroupInfo().get_cached(group_id=a.ship_group_id)
                a.ship_group_name = esi
                a.ship_category_id = esi
                esi = CategoryInfo().get_cached(category_id=a.ship_category_id)
                a.ship_category_name = esi
                esi = PricesList().get_cached()
                a.ship_adjusted_price = esi
            if a.weapon_type_id:
                esi = TypeInfo().get_cached(type_id=a.weapon_type_id)
                a.weapon_type_name = esi
                a.weapon_group_id = esi
                esi = GroupInfo().get_cached(group_id=a.weapon_group_id)
                a.weapon_group_name = esi
                a.weapon_category_id = esi
                esi = CategoryInfo().get_cached(category_id=a.weapon_category_id)
                a.weapon_category_name = esi
                esi = PricesList().get_cached()
                a.weapon_adjusted_price = esi

        EnqueueMailToStreams().apply_async(kwargs={"mail_json": m.to_json()}, ignore_result=True)
