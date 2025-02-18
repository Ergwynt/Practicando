from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField()

    def __str__(self):
        return f'Name: {self.name}'
