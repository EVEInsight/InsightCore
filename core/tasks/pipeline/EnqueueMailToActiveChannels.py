from core.celery import app
from core.models.Mail.Mail import Mail


@app.task(bind=True, max_retries=3, default_retry_delay=60 * 1, autoretry_for=(Exception,))
def EnqueueMailToActiveChannels(self, mail_json) -> None:
    """
    get active channels and queue up filter tasks with a mail
    :rtype: None
    """
    m = Mail.from_json(mail_json)
    print(f"{m.id} - parsed - {m.parsed_time}")

