from InsightCore.tasks.BaseTasks.InsightCoreTask import InsightCoreTask
from InsightCore.models.Mail import Mail
from InsightCore.models.Stream import Stream
from InsightCore.models.Visual import BaseVisual
from .PostDiscord import PostDiscord
import warnings


class StreamFiltersStage2(InsightCoreTask):
    autoretry_for = (Exception,)
    max_retries = 5
    retry_backoff = 60
    retry_backoff_max = 600
    retry_jitter = False

    def run(self, mail_json, stream_json) -> None:
        # todo docs and system filters
        m = Mail.from_json(mail_json)
        s = Stream.from_json(stream_json)
        post_cls = BaseVisual.get_cls(visual_type=s.post.visual_type, visual_id=s.post.visual_id)
        p = post_cls(mail=m, stream=s, visual_type=s.post.visual_type, visual_id=s.post.visual_id)
        if p.get_visual_type() == "discord":
            PostDiscord().apply_async(kwargs={"post_json": p.to_json()}, ignore_result=True)
        elif p.get_visual_type() == "slack":
            pass  # todo add slack webhook support
            # PostSlack().apply_async(kwargs={"post_json": p.to_json()}, ignore_result=True)
        else:
            msg = f"Visual not routed as it has an unexpected type: {p.get_visual_type()}"
            warnings.warn(msg)
