from django.db import models

from ingredients.models import Ingredient


class Recipe(models.Model):
    name = models.CharField(max_length=30, unique=True)
    script = models.TextField()
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes')

    def __str__(self):
        return f'Name: {self.name}, Script: {self.script}'


class Factor(models.Model):
    class Unit(models.TextChoices):
        PIECE = 'P', 'Piece'
        LITER = 'L', 'Liter'
        GRAM = 'G', 'Gram'

    recipe = models.ForeignKey(Recipe, related_name='recipe', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, related_name='ingredient', on_delete=models.CASCADE)
    amount = models.FloatField()
    unit = models.CharField(max_length=1, choices=Unit)

    class Meta:
        unique_together = ('recipe', 'ingredient')

    def __str__(self):
        return f'{self.amount} {self.get_unit_display()}, Ingredients: {self.ingredient}'
