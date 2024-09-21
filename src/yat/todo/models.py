from collections.abc import Sequence
from typing import Iterable, TYPE_CHECKING, cast

from django.db import models

from returns.io import impure_safe

if TYPE_CHECKING:
    from todo.models import Item


class ItemManager(models.Manager):

    def toggle(self, pk: int):
        obj = self.get(pk=pk)
        obj.done = not obj.done
        obj.save()

        return obj

    def unchecked(self):
        return self.filter(done=False)

    def checked(self):
        return self.filter(done=True)

    @impure_safe
    def batch_toggle(self, pks: Iterable[int]) -> Sequence["Item"]:
        self.filter(pk__in=pks).update(done=not models.F("done"))
        return cast(Sequence, self.filter(pk__in=pks))

    @impure_safe
    def batch_delete(self, pks: Iterable[int]) -> None:
        self.filter(pk__in=pks).delete()


class Item(models.Model):
    """
    Reprents one single to-do list item
    """

    title = models.TextField()
    description = models.TextField()
    done = models.BooleanField(default=False)

    objects: ItemManager = ItemManager()
