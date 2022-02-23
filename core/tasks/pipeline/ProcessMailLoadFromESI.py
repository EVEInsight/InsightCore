from core.celery import app
from core.models.Mail.Mail import Mail, RedisQMail
from .EnqueueMailToActiveChannels import EnqueueMailToActiveChannels
from core.tasks.ESI.GetCharacterPublicInfo import get_cached_character_public_info


@app.task(bind=True, max_retries=10, default_retry_delay=5, autoretry_for=(Exception,))
def ProcessMailLoadFromESI(self, mail_json) -> None:
    """Enqueue all ESI calls to resolve data that isn't present from ZK.

    :param self: Celery self reference required for retries.
    :param mail_json: json dictionary containing RedisQ ZK data.
    :type mail_json: dict
    :rtype: None
    """
    m = Mail.from_json(RedisQMail.from_json(mail_json).to_json())
    if m.victim.character_id:
        public_info = get_cached_character_public_info(m.victim.character_id)
        m.victim.character_name = public_info.get("name", "UnknownName") if public_info else "UnknownName"
    for a in m.attackers:
        if a.character_id:
            public_info = get_cached_character_public_info(a.character_id)
            a.character_name = public_info.get("name", "UnknownName") if public_info else "UnknownName"
    EnqueueMailToActiveChannels.apply_async(kwargs={"mail_json": m.to_json()}, ignore_result=True)
