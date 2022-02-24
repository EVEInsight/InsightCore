import os


def get_broker_url():
    """read env vars for rabbit mq to generate connect url"""
    user = os.environ["MessageQueueUser"]
    password = os.environ["MessageQueuePassword"]
    host = os.environ["MessageQueueHost"]
    port = os.environ["MessageQueuePort"]
    vhost = os.environ["MessageQueueVhost"]
    return f"amqp://{user}:{password}@{host}:{port}/{vhost}"


def get_redis_url():
    """read env vars for redis to generate connect url"""
    user = os.environ["RedisUser"]
    password = os.environ["RedisPassword"]
    host = os.environ["RedisHost"]
    port = os.environ["RedisPort"]
    db = os.environ["RedisDb"]
    return f"redis://{user}:{password}@{host}:{port}/{db}"


broker_url = get_broker_url()
result_backend = get_redis_url()
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
enable_utc = True
include = ["core.tasks.pipeline.GetMailRedisQ",
           "core.tasks.pipeline.ProcessMailEnqueueESICalls",
           "core.tasks.pipeline.ProcessMailLoadFromESI",
           "core.tasks.pipeline.EnqueueMailToActiveChannels",
           "core.tasks.ESI.CharacterPublicInfo",
           "core.tasks.ESI.CorporationInfo",
           "core.tasks.ESI.AllianceInfo"]
task_default_queue = "CeleryDefault"
task_routes = {"core.tasks.pipeline.GetMailRedisQ.*": {"queue": "GetMailRedisQ"},
               "core.tasks.pipeline.ProcessMailEnqueueESICalls.*": {"queue": "ProcessMailEnqueueESICalls"},
               "core.tasks.pipeline.ProcessMailLoadFromESI.*": {"queue": "ProcessMailLoadFromESI"},
               "core.tasks.pipeline.EnqueueMailToActiveChannels.*": {"queue": "EnqueueMailToActiveChannels"},
               "core.tasks.ESI.CharacterPublicInfo.*": {"queue": "GetCharacterPublicInfo"},
               "core.tasks.ESI.CorporationInfo.*": {"queue": "GetCorporationInfo"},
               "core.tasks.ESI.AllianceInfo.*": {"queue": "GetAllianceInfo"}
               }
# task_annotations = {"core.tasks.ESI.GetCharacterPublicInfo.GetCharacterPublicInfo": {'rate_limit': '1/s'},
#                     "core.tasks.ESI.GetCharacterPublicInfo.GetCorporationInfo": {'rate_limit': '1/s'},
#                     "core.tasks.ESI.GetCharacterPublicInfo.GetAllianceInfo": {'rate_limit': '1/s'}}
beat_schedule = {
    "get-mail-redisq": {
        "task": "core.tasks.pipeline.GetMailRedisQ.GetMailRedisQ",
        "schedule": 1,
        "options": {
            "ignore_result": True,
            "expires": 3
        }
    },
}
