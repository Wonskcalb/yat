from collections.abc import Sequence
from typing import Literal
from ninja import FilterSchema, Schema


class ErrorBody(Schema):
    type: str
    loc: list | int
    msg: str
    ctx: dict


class PydanticError(Schema):
    detail: list[ErrorBody]


class Message(Schema):
    message: str


class Error(Schema):
    error: str


class ItemFilter(FilterSchema):
    state: Literal["all", "checked", "unchecked"] = "unchecked"


class ItemIn(Schema):
    title: str
    description: str


class ItemOut(Schema):
    id: int
    title: str
    description: str
    done: bool

    class Config:
        from_attributes = True


class BaseAction(Schema):
    action: Literal["toggle", "delete"]


class ActionIn(BaseAction):
    ids: list[int]


class ActionOut(BaseAction):
    error: ErrorBody | None = None
    items: Sequence[ItemOut] | None = None
