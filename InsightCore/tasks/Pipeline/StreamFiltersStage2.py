from InsightCore.tasks.BaseTasks.InsightCoreTask import InsightCoreTask
from InsightCore.models.Mail import Mail
from InsightCore.models.Stream import Stream
from InsightCore.models.PostContent import DiscordText
from .PostDiscord import PostDiscord


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
        p = DiscordText(mail=m, stream=s)
        PostDiscord().apply_async(kwargs={"post_json": p.to_json()}, ignore_result=True)
