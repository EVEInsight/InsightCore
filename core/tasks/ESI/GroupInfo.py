from core.celery import app
from core.tasks.BaseTasks.BaseTask import BaseTask
from .ESIResqust import ESIRequest
from celery.result import AsyncResult
from core.exceptions.ESI import InputValidationError
from .CategoryInfo import CategoryInfo


class GroupInfo(ESIRequest):
    @classmethod
    def get_key(cls, group_id: int):
        return f"GroupInfo-{group_id}"

    @classmethod
    def route(cls, group_id: int):
        return f"/universe/groups/{group_id}"

    @classmethod
    def _get_celery_async_result(cls, ignore_result: bool = False, **kwargs) -> AsyncResult:
        return GetGroupInfo.apply_async(kwargs=kwargs, ignore_result=ignore_result)

    @classmethod
    def _hook_after_esi_success(cls, esi_response: dict) -> None:
        category_id = esi_response.get("category_id")
        if category_id:
            CategoryInfo.get_async(ignore_result=True, category_id=category_id)

    @classmethod
    def validate_inputs(cls, group_id: int) -> None:
        try:
            int(group_id)
        except ValueError:
            raise InputValidationError("Input parameter must be an integer.")


@app.task(base=BaseTask, bind=True, max_retries=3, retry_backoff=5, autoretry_for=(Exception,))
def GetGroupInfo(self, **kwargs) -> dict:
    """Gets the cached response or call ESI to get data.

    :param self: self reference for celery retries
    :param kwargs: ESI request parameters
    :return: Dictionary containing response from ESI.
    :rgroup: dict
    """
    return GroupInfo._request_esi(GetGroupInfo.redis, **kwargs)
