from django import forms

from .models import Ingredient


class AddIngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ('name', 'description')
