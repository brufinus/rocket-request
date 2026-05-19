from django.db import models


class Item(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    stack_size = models.IntegerField()
    rocket_capacity = models.IntegerField()
    weight = models.FloatField()

    def __str__(self) -> str:
        return self.name


class Keywords(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=30, unique=True)

    def __str__(self) -> str:
        return self.keyword
