from django.shortcuts import get_object_or_404, redirect, render

from .forms import FactorForm, RecipeForm
from .models import Factor, Recipe


def recipes_list(request):
    recipes = Recipe.objects.all()

    return render(request, 'recipes/recipes_list.html', {'recipes': recipes})


def recipes_detail(request, pk):
    recipes_detail = Recipe.objects.get(pk=pk)
    factor_list = Factor.objects.all()
    return render(
        request, 'recipes/recipes_detail.html', {'recipe': recipes_detail, 'factors': factor_list}
    )


def add_recipes(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save()
            return redirect('recipes:recipes-detail', pk=recipe.pk)
    else:
        form = RecipeForm()

    return render(request, 'recipes/add_recipes.html', {'form': form})


def add_factor(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        form = FactorForm(request.POST)
        if form.is_valid():
            factor = form.save(commit=False)
            factor.recipe = recipe  # Asignar la receta al factor
            factor.save()
            return redirect(
                'recipes:recipes-detail', recipe_id=recipe.pk
            )  # Redirigir al detalle de la receta
    else:
        form = FactorForm()

    return render(request, 'recipes/add_factor.html', {'form': form, 'recipe': recipe})
