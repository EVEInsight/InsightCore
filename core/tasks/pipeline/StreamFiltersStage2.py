from core.celery import app
from core.tasks.BaseTasks.BaseTask import BaseTask
from core.models.Mail.Mail import Mail
from core.models.Stream.Stream import Stream


@app.task(base=BaseTask, bind=True, max_retries=5, default_retry_delay=60, autoretry_for=(Exception,))
def StreamFiltersStage2(self, mail_json, stream_json) -> None:
    m = Mail.from_json(mail_json)
    s = Stream.from_json(stream_json)
    print(m.id)
    # todo queue post call
    return


