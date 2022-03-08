from core.tasks.BaseTasks.InsightCoreTask import InsightCoreTask
from core.models.Mail.Mail import Mail


class StreamFiltersStage2(InsightCoreTask):
    autoretry_for = (Exception,)
    max_retries = 5
    retry_backoff = 60
    retry_backoff_max = 600
    retry_jitter = False

    def run(self, mail_json, stream_json) -> None:
        m = Mail.from_json(mail_json)
        print(m.id)
        # todo queue post call
        return
