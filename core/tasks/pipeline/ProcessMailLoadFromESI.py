from core.celery import app
from core.models.Mail.Mail import Mail
from .EnqueueMailToActiveChannels import EnqueueMailToActiveChannels
from core.tasks.ESI.GetCharacterPublicInfo import get_cached_character_public_info


@app.task(bind=True, max_retries=3, default_retry_delay=1, autoretry_for=(Exception,))
def ProcessMailLoadFromESI(self, mail_json) -> None:
    """
    covert a mail to model and resolve names
    :rtype: None
    """
    m = Mail.from_json(mail_json)
    if m.victim.character_id:
        public_info = get_cached_character_public_info(m.victim.character_id)
        m.victim.character_name = public_info.get("name", "UnknownName") if public_info else "UnknownName"
    for a in m.attackers:
        if a.character_id:
            public_info = get_cached_character_public_info(a.character_id)
            a.character_name = public_info.get("name", "UnknownName") if public_info else "UnknownName"
    EnqueueMailToActiveChannels.apply_async(kwargs={"mail_json": m.to_json()}, ignore_result=True)
