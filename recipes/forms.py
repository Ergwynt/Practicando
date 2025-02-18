from django import forms

from .models import Factor, Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'script']


class FactorForm(forms.ModelForm):
    class Meta:
        model = Factor
        fields = ['ingredient', 'amount', 'unit']
