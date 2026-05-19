"""Models to represent in-game items."""

from django.db import models


class Item(models.Model):
    """Model for item data."""

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    stack_size = models.IntegerField()
    rocket_capacity = models.IntegerField()
    weight = models.FloatField()
    name_slug = models.SlugField(max_length=30, unique=True, null=True)

    def __str__(self) -> str:
        return self.name


class Keywords(models.Model):
    """Relational model for item keywords."""

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=30, unique=True)

    def __str__(self) -> str:
        return self.keyword
