from django.shortcuts import get_object_or_404, redirect, render

from .forms import AddIngredientForm
from .models import Ingredient


def ingredient_list(request):
    ingredients = Ingredient.objects.all()

    return render(request, 'ingredients/ingredient_list.html', {'ingredients': ingredients})


def ingredients_detail(request, pk):
    ingredient_detail = get_object_or_404(Ingredient, pk=pk)

    return render(request, 'ingredients/ingredient_detail.html', {'ingredients': ingredient_detail})


def ingredients_add(request):
    if request.method == 'POST':
        form = AddIngredientForm(request.POST)
        if form.is_valid():
            ingredient = form.save()
            return redirect('ingredient:ingredient-list')
    else:
        form = AddIngredientForm()

    return render(
        request,
        'ingredients/add_ingredients.html',
        {
            'form': form,
        },
    )
