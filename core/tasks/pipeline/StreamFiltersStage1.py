from core.celery import app
from core.tasks.BaseTasks.BaseTask import BaseTask
from .StreamFiltersStage2 import StreamFiltersStage2
from dateutil.parser import parse as dtparse
from datetime import datetime


@app.task(base=BaseTask, bind=True, max_retries=3, default_retry_delay=5, autoretry_for=(Exception,))
def StreamFiltersStage1(self, mail_json: dict, stream_json: dict) -> None:
    f = stream_json["filter"]
    if f["_km_require_npc"] and not mail_json["zkb_npc"]:
        return
    if f["_km_require_solo"] and not mail_json["zkb_solo"]:
        return
    if f["_km_require_awox"] and not mail_json["zkb_awox"]:
        return

    if not (f["_km_min_fittedValue"] <= mail_json["zkb_fittedValue"] <= f["_km_max_fittedValue"]):
        return
    if not (f["_km_min_droppedValue"] <= mail_json["zkb_droppedValue"] <= f["_km_max_droppedValue"]):
        return
    if not (f["_km_min_destroyedValue"] <= mail_json["zkb_destroyedValue"] <= f["_km_max_destroyedValue"]):
        return
    if not (f["_km_min_totalValue"] <= mail_json["zkb_totalValue"] <= f["_km_max_totalValue"]):
        return

    if not (f["_km_min_points"] <= mail_json["zkb_points"] <= f["_km_max_points"]):
        return

    if not (f["_km_min_age_seconds"]
            <= (datetime.utcnow() - dtparse(mail_json["killmail_time"], ignoretz=True)).total_seconds()
            <= f["_km_max_age_seconds"]):
        return
    if not (f["_km_min_points"] <= mail_json["zkb_points"] <= f["_km_max_points"]):
        return

    if not (f["_system_min_security_status"]
            <= mail_json["_system_security_status"]
            <= f["_system_max_security_status"]):
        return

    alliance_ids = set(f["_victim_alliance_ids_include"]) - set(f["_victim_alliance_ids_exclude"])
    if mail_json["victim"]["alliance_id"] not in alliance_ids and "*" not in alliance_ids:
        return
    corporation_ids = set(f["_victim_corporation_ids_include"]) - set(f["_victim_corporation_ids_exclude"])
    if mail_json["victim"]["corporation_id"] not in corporation_ids and "*" not in corporation_ids:
        return
    character_ids = set(f["_victim_character_ids_include"]) - set(f["_victim_character_ids_exclude"])
    if mail_json["victim"]["character_id"] not in character_ids and "*" not in character_ids:
        return
    faction_ids = set(f["_victim_faction_ids_include"]) - set(f["_victim_faction_ids_exclude"])
    if mail_json["victim"]["faction_id"] not in faction_ids and "*" not in faction_ids:
        return
    _ship_category_ids = set(f["_victim_ship_category_ids_include"]) - set(f["_victim_ship_category_ids_exclude"])
    if mail_json["victim"]["_ship_category_id"] not in _ship_category_ids and "*" not in _ship_category_ids:
        return

    region_ids = set(f["_region_ids_include"]) - set(f["_region_ids_exclude"])
    if mail_json["_region_id"] not in region_ids and "*" not in region_ids:
        return
    constellation_ids = set(f["_constellation_ids_include"]) - set(f["_constellation_ids_exclude"])
    if mail_json["_constellation_id"] not in constellation_ids and "*" not in constellation_ids:
        return
    system_ids = set(f["_system_ids_include"]) - set(f["_system_ids_exclude"])
    if mail_json["system_id"] not in system_ids and "*" not in system_ids:
        return
    location_ids = set(f["_location_ids_include"]) - set(f["_location_ids_exclude"])
    if mail_json["zkb_locationID"] not in location_ids and "*" not in location_ids:
        return

    # todo update details for post object
    StreamFiltersStage2.apply_async(kwargs={"mail_json": mail_json, "stream_json": stream_json}, ignore_result=True)

