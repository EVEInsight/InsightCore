from InsightCore.tasks.BaseTasks.InsightCoreTask import InsightCoreTask
from .StreamFiltersStage2 import StreamFiltersStage2
from datetime import datetime
from InsightCore.models.Mail.Mail import Mail
from InsightCore.models.Stream.Stream import Stream
from ESICelery.tasks.Routes import Route
from ESICelery.tasks.Universe import SystemInfo


class StreamFiltersStage1(InsightCoreTask):
    autoretry_for = (Exception,)
    max_retries = 3
    retry_backoff = 60
    retry_backoff_max = 600
    retry_jitter = False

    @classmethod
    def filter(cls, filter_ids_include, filter_ids_exclude, mail_id) -> bool:
        """Checks if the ID from a mail exists in filter_ids_include after removing filter_ids_exclude

        :param filter_ids_include: The match filter ids of integers. Can include the "*" wildcard string to match all.
        :type filter_ids_include: list[int]
        :param filter_ids_exclude: The excluded filter ids of integers.
        :type filter_ids_exclude: list[int]
        :param mail_id: The comparison id that must exist in set(filter_ids_include) - set(filter_ids_exclude)
        :return: True if mail_id exists in set(filter_ids_include) - set(filter_ids_exclude) else False
        """
        set_filter_ids_include = set(filter_ids_include)
        set_filter_ids_exclude = set(filter_ids_exclude)
        filter_ids = set_filter_ids_include - set_filter_ids_exclude
        if "*" in set_filter_ids_include and mail_id not in set_filter_ids_exclude:
            return True
        elif "*" in set_filter_ids_include and mail_id in set_filter_ids_exclude:
            return False
        elif mail_id in filter_ids:
            return True
        else:
            return False

    def run(self, mail_json: dict, stream_json: dict) -> None:
        """Check filters for a stream against a mail. If all filters pass then move to next stage.
        If the stream does not pass a single filter then it is discarded.

        :param self: Celery self reference required for retries.
        :param mail_json: Mail json
        :param stream_json: Steam json
        :rtype: None
        """
        m = Mail.from_json(mail_json)
        s = Stream.from_json(stream_json)
        f = s.filter

        # zk detail filters
        if f.km_require_npc and not m.zkb_npc:
            return
        if f.km_require_solo and not m.zkb_solo:
            return
        if f.km_require_awox and not m.zkb_awox:
            return
        if not (f.km_min_points <= m.zkb_points <= f.km_max_points):
            return

        # price filters
        if not (f.km_min_fittedValue <= m.zkb_fittedValue <= f.km_max_fittedValue):
            return
        if not (f.km_min_droppedValue <= m.zkb_droppedValue <= f.km_max_droppedValue):
            return
        if not (f.km_min_destroyedValue <= m.zkb_destroyedValue <= f.km_max_destroyedValue):
            return
        if not (f.km_min_totalValue <= m.zkb_totalValue <= f.km_max_totalValue):
            return

        # time filters
        if not (f.km_min_age_seconds <= (datetime.utcnow() - m.killmail_time).total_seconds() <= f.km_max_age_seconds):
            return

        # target filters
        if not f.victim_min_damage_taken <= m.victim.damage_taken <= f.victim_max_damage_taken:
            return
        if not self.filter(f.victim_alliance_ids_include, f.victim_alliance_ids_exclude, m.victim.alliance_id):
            return
        if not self.filter(f.victim_corporation_ids_include, f.victim_corporation_ids_exclude, m.victim.corporation_id):
            return
        if not self.filter(f.victim_character_ids_include, f.victim_character_ids_exclude, m.victim.character_id):
            return
        if not self.filter(f.victim_faction_ids_include, f.victim_faction_ids_exclude, m.victim.faction_id):
            return
        if not self.passes_filter(f.victim_ship_category_ids_include, f.victim_ship_category_ids_exclude,
                                  m.victim.ship_category_id):
            return
        if not self.filter(f.victim_ship_group_ids_include, f.victim_ship_group_ids_exclude,
                           m.victim.ship_group_id):
            return
        if not self.filter(f.victim_ship_type_ids_include, f.victim_ship_type_ids_exclude,
                           m.victim.ship_type_id):
            return

        # location / system filter
        # Remaining filters for systems require ESI lookups done in next filter stage
        if not (f.system_min_security_status <= m.system_security_status <= f.system_max_security_status):
            return
        if not self.filter(f.region_ids_include, f.region_ids_exclude, m.region_id):
            return
        if not self.filter(f.constellation_ids_include, f.constellation_ids_exclude, m.constellation_id):
            return
        if not self.filter(f.location_ids_include, f.location_ids_exclude, m.zkb_locationID):
            return
        if m.system_id in f.system_ids_exclude:
            return

        for system_gate in f.system_ranges_gate_include:
            Route().get_async(ignore_result=True, origin=system_gate.system_id, destinatio=m.system_id)
        for system_lightyear in f.system_ranges_lightyear_include:
            SystemInfo().get_async(ignore_result=True, system_id=system_lightyear.system_id)

        StreamFiltersStage2().apply_async(kwargs={"mail_json": mail_json, "stream_json": stream_json},
                                          ignore_result=True)
