from django.shortcuts import get_object_or_404
from ninja import Query, Router
from returns.io import IOFailure, IOSuccess
from returns.result import Failure, Success

from . import schema, models
from .exceptions import BatchException

router = Router()


@router.post("/", response=schema.ItemOut)
def create_item(request, payload: schema.ItemIn):
    return models.Item.objects.create(**payload.dict())


@router.get("/", response=list[schema.ItemOut])
def list_items(request, filters: schema.ItemFilter = Query(...)):
    """
    List items either all, done, or pending (default)
    """

    if filters.state == "all":
        return models.Item.objects.all()

    elif filters.state == "unchecked":
        return models.Item.objects.unchecked()

    elif filters.state == "checked":
        return models.Item.objects.checked()


@router.post("/batch/",
             response={200: list[schema.ActionOut], 422: schema.PydanticError})
def batch_action(request, payload: list[schema.ActionIn]):
    """
    Run an action on multiple items at once
    """
    response = []

    for batch in payload:
        match batch.action:
            case "toggle":
                action = models.Item.objects.batch_toggle
            case "delete":
                action = models.Item.objects.batch_delete
            case invalid_action:
                response.append(
                    schema.ActionOut(
                        action=batch.action,
                        error=schema.ErrorBody.model_validate(
                            BatchException(f"{invalid_action} is not a valid action")
                        )
                    )
                )
                continue

        outcome = action(batch.ids)

        match outcome:
            case IOSuccess(Success(None)):
                response.append(schema.ActionOut(action=batch.action))
            case IOSuccess(Success(objects)) if objects is not None:
                response.append(
                    schema.ActionOut(
                        action=batch.action,
                        items=[schema.ItemOut.model_validate(obj) for obj in objects]
                    )
                )
            case IOFailure(Failure(exception)):
                response.append(
                    schema.ActionOut(
                        action=batch.action,
                        error=schema.ErrorBody.model_validate(exception)
                    )
                )


@router.get("/{item_id}/", response=schema.ItemOut)
def get_item(request, item_id: int):
    """
    Return an item.
    """

    return get_object_or_404(models.Item, id=item_id)


@router.delete("/{item_id}/", response={204: schema.Message, 404: schema.Error})
def delete_item(request, item_id: int):
    """
    Delete an item from the list.
    """

    obj = get_object_or_404(models.Item, id=item_id)
    obj.delete()

    return 204, {"message": "Deleted"}


@router.post("/{item_id}/toggle/", response=schema.ItemOut)
def toggle_item_state(request, item_id: int):
    """
    Toggle the state of an item.

    A pending item will be marked as done and vice-versa.
    """
    return models.Item.objects.toggle(item_id)
