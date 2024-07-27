from typing import Literal
from ninja import FilterSchema, Schema


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


class ActionIn(Schema):
    action: Literal["toggle", "delete"]
    ids: list[int]


class ErrorBody(Schema):
    type: str
    loc: list | int
    msg: str
    ctx: dict


class PydanticError(Schema):
    detail: list[ErrorBody]

