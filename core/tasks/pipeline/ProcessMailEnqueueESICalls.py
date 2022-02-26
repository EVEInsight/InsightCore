from core.celery import app
from core.models.Mail.Mail import RedisQMail
from core.tasks.ESI.CharacterPublicInfo import CharacterPublicInfo
from core.tasks.ESI.CorporationInfo import CorporationInfo
from core.tasks.ESI.AllianceInfo import AllianceInfo
from core.tasks.ESI.SystemInfo import SystemInfo
from core.tasks.ESI.TypeInfo import TypeInfo
from core.tasks.ESI.FactionsList import FactionsList


@app.task(bind=True, max_retries=3, default_retry_delay=60*1, autoretry_for=(Exception,))
def ProcessMailEnqueueESICalls(self, mail_json: dict) -> None:
    """Enqueue all ESI calls to resolve data that isn't present from ZK.

    :param self: Celery self reference required for retries.
    :param mail_json: json dictionary containing data directly from RedisQ ZK.
    :type mail_json: dict
    :rtype: None
    """
    m = RedisQMail.from_json(mail_json)

    if m.system_id:
        SystemInfo.get_async(ignore_result=True, system_id=m.system_id)

    if m.victim:
        if m.victim.character_id:
            CharacterPublicInfo.get_async(ignore_result=True, character_id=m.victim.character_id)
        if m.victim.corporation_id:
            CorporationInfo.get_async(ignore_result=True, corporation_id=m.victim.corporation_id)
        if m.victim.alliance_id:
            AllianceInfo.get_async(ignore_result=True, alliance_id=m.victim.alliance_id)
        if m.victim.faction_id:
            FactionsList.get_async(ignore_result=True)
        if m.victim.ship_type_id:
            TypeInfo.get_async(ignore_result=True, type_id=m.victim.ship_type_id)

    for a in m.attackers:
        if a.character_id:
            CharacterPublicInfo.get_async(ignore_result=True, character_id=a.character_id)
        if a.corporation_id:
            CorporationInfo.get_async(ignore_result=True, corporation_id=a.corporation_id)
        if a.alliance_id:
            AllianceInfo.get_async(ignore_result=True, alliance_id=a.alliance_id)
        if a.faction_id:
            FactionsList.get_async(ignore_result=True)
        if a.ship_type_id:
            TypeInfo.get_async(ignore_result=True, type_id=a.ship_type_id)
        if a.weapon_type_id:
            TypeInfo.get_async(ignore_result=True, type_id=a.weapon_type_id)

