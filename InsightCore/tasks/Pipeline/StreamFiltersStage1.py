from InsightCore.tasks.BaseTasks.InsightCoreTask import InsightCoreTask
from .StreamFiltersStage2 import StreamFiltersStage2
from datetime import datetime
from InsightCore.models.Mail.Mail import Mail
from InsightCore.models.Stream.Stream import Stream
from InsightCore.models.Stream.Filter import Filter
from InsightCore.models.Visual import BaseVisual
from InsightCore.utils import Filters
from ESICelery.tasks.Routes import Route
from ESICelery.tasks.Universe import SystemInfo


class StreamFiltersStage1(InsightCoreTask):
    autoretry_for = (Exception,)
    max_retries = 3
    retry_backoff = 60
    retry_backoff_max = 600
    retry_jitter = False

    @classmethod
    def filter_mail(cls, f: Filter, m: Mail):
        # zk detail filters
        if f.km_require_npc and not m.zkb_npc:
            return False
        if f.km_require_solo and not m.zkb_solo:
            return False
        if f.km_require_awox and not m.zkb_awox:
            return False
        if not f.km_min_points <= m.zkb_points <= f.km_max_points:
            return False
        # price filters
        if not f.km_min_fittedValue <= m.zkb_fittedValue <= f.km_max_fittedValue:
            return False
        if not f.km_min_droppedValue <= m.zkb_droppedValue <= f.km_max_droppedValue:
            return False
        if not f.km_min_destroyedValue <= m.zkb_destroyedValue <= f.km_max_destroyedValue:
            return False
        if not f.km_min_totalValue <= m.zkb_totalValue <= f.km_max_totalValue:
            return False
        # time filters
        if not f.km_min_age_seconds <= (datetime.utcnow() - m.killmail_time).total_seconds() <= f.km_max_age_seconds:
            return False
        if not f.km_attackers_min <= m.involved <= f.km_attackers_max:
            return False
        return True

    @classmethod
    def filter_attackers(cls, f: Filter, m: Mail):
        matched = []
        for a in m.attackers:
            if not f.attacker_min_security_status <= a.security_status <= f.attacker_max_security_status:
                continue
            if not f.attacker_min_damage_done <= a.damage_done <= f.attacker_max_damage_done:
                continue
            if not Filters.filter_ids(f.attacker_alliance_ids_include, f.attacker_alliance_ids_exclude,
                                      a.alliance_id):
                continue
            if not Filters.filter_ids(f.attacker_corporation_ids_include, f.attacker_corporation_ids_exclude,
                                      a.corporation_id):
                continue
            if not Filters.filter_ids(f.attacker_character_ids_include, f.attacker_character_ids_exclude,
                                      a.character_id):
                continue
            if not Filters.filter_ids(f.attacker_faction_ids_include, f.attacker_faction_ids_exclude,
                                      a.faction_id):
                continue
            if not Filters.filter_ids(f.attacker_ship_category_ids_include, f.attacker_ship_category_ids_exclude,
                                      a.ship_category_id):
                continue
            if not Filters.filter_ids(f.attacker_ship_group_ids_include, f.attacker_ship_group_ids_exclude,
                                      a.ship_group_id):
                continue
            if not Filters.filter_ids(f.attacker_ship_type_ids_include, f.attacker_ship_type_ids_exclude,
                                      a.ship_type_id):
                continue
            if not Filters.filter_ids(f.attacker_weapon_category_ids_include, f.attacker_weapon_category_ids_exclude,
                                      a.weapon_category_id):
                continue
            if not Filters.filter_ids(f.attacker_weapon_group_ids_include, f.attacker_weapon_group_ids_exclude,
                                      a.weapon_group_id):
                continue
            if not Filters.filter_ids(f.attacker_weapon_type_ids_include, f.attacker_weapon_type_ids_exclude,
                                      a.weapon_type_id):
                continue
            matched.append(a)
        return matched

    @classmethod
    def filter_victim(cls, f: Filter, m: Mail):
        if not f.victim_min_damage_taken <= m.victim.damage_taken <= f.victim_max_damage_taken:
            return False
        if not Filters.filter_ids(f.victim_alliance_ids_include, f.victim_alliance_ids_exclude, m.victim.alliance_id):
            return False
        if not Filters.filter_ids(f.victim_corporation_ids_include, f.victim_corporation_ids_exclude,
                                  m.victim.corporation_id):
            return False
        if not Filters.filter_ids(f.victim_character_ids_include, f.victim_character_ids_exclude,
                                  m.victim.character_id):
            return False
        if not Filters.filter_ids(f.victim_faction_ids_include, f.victim_faction_ids_exclude,
                                  m.victim.faction_id):
            return False
        if not Filters.filter_ids(f.victim_ship_category_ids_include, f.victim_ship_category_ids_exclude,
                                  m.victim.ship_category_id):
            return False
        if not Filters.filter_ids(f.victim_ship_group_ids_include, f.victim_ship_group_ids_exclude,
                                  m.victim.ship_group_id):
            return False
        if not Filters.filter_ids(f.victim_ship_type_ids_include, f.victim_ship_type_ids_exclude,
                                  m.victim.ship_type_id):
            return False
        return True

    @classmethod
    def filter_universe(cls, f: Filter, m: Mail):
        if not f.system_min_security_status <= m.system_security_status <= f.system_max_security_status:
            return False
        if not Filters.filter_ids(f.region_ids_include, f.region_ids_exclude, m.region_id):
            return False
        if not Filters.filter_ids(f.constellation_ids_include, f.constellation_ids_exclude, m.constellation_id):
            return False
        if not Filters.filter_ids(f.location_ids_include, f.location_ids_exclude, m.zkb_locationID):
            return False
        if m.system_id in f.system_ids_exclude:
            return False
        return True

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
        matched_attackers = []
        is_loss = False
        passes_victim_filter = False

        if not self.filter_mail(f, m):
            return

        # target filters
        if not self.filter_victim(f, m):
            if f.operator_attacker_victim_and:
                return
            else:
                is_loss = False
        else:
            passes_victim_filter = True
            if f.operator_attacker_victim_and:
                is_loss = False
            else:
                is_loss = True

        # attackers filter
        matched_attackers = self.filter_attackers(f, m)
        if f.operator_attacker_victim_and:
            if len(matched_attackers) == 0:
                return
            if m.involved > 0 and len(matched_attackers) / m.involved < f.attackers_ratio_min:
                return
        else:
            if not passes_victim_filter:
                if len(matched_attackers) == 0:
                    return
                if m.involved > 0 and len(matched_attackers) / m.involved < f.attackers_ratio_min:
                    return

        if not self.filter_universe(f, m):
            return

        visual_cls = BaseVisual.get_cls(visual_type=s.post.visual_type, visual_id=s.post.visual_id)
        visual = visual_cls(mail=m, stream=s, visual_type=s.post.visual_type, visual_id=s.post.visual_id,
                            filtered_attackers=matched_attackers, is_loss=is_loss)
        visual_json = visual.to_json()
        for system_gate in f.system_ranges_gate_include:
            Route().get_async(ignore_result=True, origin=system_gate.system_id, destination=m.system_id)
        for system_lightyear in f.system_ranges_lightyear_include:
            SystemInfo().get_async(ignore_result=True, system_id=system_lightyear.system_id)

        StreamFiltersStage2().apply_async(kwargs={"visual_json": visual_json}, ignore_result=True)
