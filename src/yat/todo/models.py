from typing import Iterable
from django.db import models


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


    def batch_toggle(self, pks: Iterable[int]):
        self.filter(pk__in=pks).update(done=not models.F("done"))
        return self.filter(pk__in=pks)

class Item(models.Model):
    """
    Reprents one single to-do list item
    """

    title = models.TextField()
    description = models.TextField()
    done = models.BooleanField(default=False)

    objects: ItemManager = ItemManager()
