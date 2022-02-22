from core.celery import app
from core.models.Mail.Mail import Mail
from .EnqueueMailToActiveChannels import EnqueueMailToActiveChannels


@app.task(bind=True, max_retries=3, default_retry_delay=60*1, autoretry_for=(Exception,))
def ProcessMail(self, mail_json) -> None:
    """
    covert a mail to model and resolve names
    :rtype: None
    """
    m = Mail.json_decode_from_zk(mail_json)
    # todo api resolve
    EnqueueMailToActiveChannels.delay(m.json_encode())
