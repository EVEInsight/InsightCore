from core.celery import app
from core.models.Mail.Mail import RedisQMail
from .ProcessMailLoadFromESI import ProcessMailLoadFromESI
from core.tasks.ESI.GetCharacterPublicInfo import GetCharacterPublicInfo


@app.task(bind=True, max_retries=3, default_retry_delay=60*1, autoretry_for=(Exception,))
def ProcessMailEnqueueESICalls(self, mail_json) -> None:
    """
    covert a mail to model and resolve names
    :rtype: None
    """
    m = RedisQMail.from_json(mail_json)
    if m.victim.character_id:
        GetCharacterPublicInfo.apply_async(kwargs={"character_id": m.victim.character_id}, ignore_result=True)
    for a in m.attackers:
        if a.character_id:
            GetCharacterPublicInfo.apply_async(kwargs={"character_id": a.character_id}, ignore_result=True)
    ProcessMailLoadFromESI.apply_async(kwargs={"mail_json": m.to_json()}, ignore_result=True)
