import pytest
from faker import Faker
from model_bakery import baker

from ingredients.models import Ingredient
from recipes.models import Factor, Recipe


@pytest.fixture
def fake():
    return Faker()


@pytest.fixture
def ingredient():
    return baker.make(Ingredient, _fill_optional=True)


@pytest.fixture
def recipe():
    return baker.make(Recipe, _fill_optional=True)


@pytest.fixture
def recipe_with_factors():
    recipe = baker.make(Recipe, _fill_optional=True)
    baker.make(Factor, recipe=recipe, _fill_optional=True, _quantity=5)
    return recipe
