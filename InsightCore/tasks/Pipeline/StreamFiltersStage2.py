from InsightCore.tasks.BaseTasks.InsightCoreTask import InsightCoreTask
from InsightCore.models.Visual import BaseVisual
from .PostDiscord import PostDiscord
import warnings


class StreamFiltersStage2(InsightCoreTask):
    autoretry_for = (Exception,)
    max_retries = 5
    retry_backoff = 60
    retry_backoff_max = 600
    retry_jitter = False

    def run(self, visual_json) -> None:
        # todo docs and system filters
        v = BaseVisual.from_json_subclass(visual_json)
        if v.get_visual_type() == "discord":
            PostDiscord().apply_async(kwargs={"post_json": v.to_json()}, ignore_result=True)
        elif v.get_visual_type() == "slack":
            pass  # todo add slack webhook support
            # PostSlack().apply_async(kwargs={"post_json": v.to_json()}, ignore_result=True)
        else:
            msg = f"Visual not routed as it has an unexpected type: {v.get_visual_type()}"
            warnings.warn(msg)
