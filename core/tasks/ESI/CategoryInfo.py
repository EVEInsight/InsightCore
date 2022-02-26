from core.celery import app
from core.tasks.BaseTasks.BaseTask import BaseTask
from .ESIResqust import ESIRequest
from celery.result import AsyncResult
from core.exceptions.ESI import InputValidationError


class CategoryInfo(ESIRequest):
    @classmethod
    def get_key(cls, category_id: int):
        return f"CategoryInfo-{category_id}"

    @classmethod
    def route(cls, category_id: int):
        return f"/universe/categories/{category_id}"

    @classmethod
    def _get_celery_async_result(cls, ignore_result: bool = False, **kwargs) -> AsyncResult:
        return GetCategoryInfo.apply_async(kwargs=kwargs, ignore_result=ignore_result)

    @classmethod
    def validate_inputs(cls, category_id: int) -> None:
        try:
            int(category_id)
        except ValueError:
            raise InputValidationError("Input parameter must be an integer.")


@app.task(base=BaseTask, bind=True, max_retries=3, retry_backoff=5, autoretry_for=(Exception,))
def GetCategoryInfo(self, **kwargs) -> dict:
    """Gets the cached response or call ESI to get data.

    :param self: self reference for celery retries
    :param kwargs: ESI request parameters
    :return: Dictionary containing response from ESI.
    :rcategory: dict
    """
    return CategoryInfo._request_esi(GetCategoryInfo.redis, **kwargs)
