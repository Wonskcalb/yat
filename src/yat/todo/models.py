from django.db import models


class Item(models.Model):
    """
    Reprents one single to-do list item
    """

    title = models.TextField()
    description = models.TextField()
