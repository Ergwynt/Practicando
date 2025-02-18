from http import HTTPStatus

import pytest
from django.db.utils import IntegrityError
from model_bakery import baker
from pytest_django.asserts import assertContains, assertRedirects

from recipes.models import Factor, Recipe


@pytest.mark.django_db
def test_recipe_list_is_properly_displayed(client):
    recipes = baker.make(Recipe, _fill_optional=True, _quantity=10)
    response = client.get('/recipes/')
    for recipe in recipes:
        assertContains(response, recipe.name)


@pytest.mark.django_db
def test_proper_message_is_shown_when_recipe_list_is_empty(client):
    response = client.get('/recipes/')
    assertContains(response, 'No recipes so far!')


@pytest.mark.django_db
def test_recipe_list_contains_links_to_recipe_detail(client):
    recipes = baker.make(Recipe, _fill_optional=True, _quantity=10)
    response = client.get('/recipes/')
    for recipe in recipes:
        href = f'href="/recipes/{recipe.pk}/"'
        assertContains(response, href)


@pytest.mark.django_db
def test_recipe_list_contains_link_to_add_recipe(client):
    response = client.get('/recipes/')
    assertContains(response, 'href="/recipes/add/"')


@pytest.mark.django_db
def test_add_recipe_form_contains_proper_fields(client):
    response = client.get('/recipes/add/')
    assertContains(response, 'Name:')
    assertContains(response, 'Script:')


@pytest.mark.django_db
def test_add_recipe_works_properly(client, fake):
    payload = {'name': fake.name(), 'script': fake.paragraph()}
    response = client.post('/recipes/add/', payload)
    recipe = Recipe.objects.get(name=payload['name'])
    assert recipe.script == payload['script']
    assertRedirects(response, f'/recipes/{recipe.pk}/')


@pytest.mark.django_db
def test_add_recipe_fails_when_name_is_duplicated(client, fake, recipe):
    payload = {'name': recipe.name, 'description': fake.paragraph()}
    response = client.post('/recipes/add/', payload)
    assertContains(response, 'Recipe with this Name already exists')


@pytest.mark.django_db
def test_recipe_detail_contains_proper_content_without_factors(client, recipe):
    response = client.get(f'/recipes/{recipe.pk}/')
    assertContains(response, recipe.name)
    assertContains(response, recipe.script)
    assertContains(response, 'No factors so far!')


@pytest.mark.django_db
def test_recipe_detail_contains_proper_content_with_factors(client, recipe_with_factors):
    response = client.get(f'/recipes/{recipe_with_factors.pk}/')
    assertContains(response, recipe_with_factors.name)
    assertContains(response, recipe_with_factors.script)
    factors = Factor.objects.filter(recipe=recipe_with_factors)
    for factor in factors:
        assertContains(response, factor.ingredient)
        assertContains(response, factor.amount)
        assertContains(response, factor.unit)


@pytest.mark.django_db
def test_recipe_detail_returns_404_when_recipe_does_not_exist(client):
    response = client.get('/recipes/1/')
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_recipe_detail_contains_link_to_add_factors(client, recipe):
    response = client.get(f'/recipes/{recipe.pk}/')
    href = f'/recipes/{recipe.pk}/add-factor/'
    assertContains(response, href)


@pytest.mark.django_db
def test_add_factor_form_contains_proper_fields(client, recipe):
    response = client.get(f'/recipes/{recipe.pk}/add-factor/')
    assertContains(response, 'Ingredient:')
    assertContains(response, 'Amount:')
    assertContains(response, 'Unit:')


@pytest.mark.django_db
def test_add_factor_works_properly(client, ingredient, recipe):
    payload = {'ingredient': ingredient.pk, 'amount': 0.5, 'unit': 'L'}
    response = client.post(f'/recipes/{recipe.pk}/add-factor/', payload)
    assertRedirects(response, f'/recipes/{recipe.pk}/')
    factor = Factor.objects.get(recipe=recipe, ingredient__pk=payload['ingredient'])
    assert factor.amount == payload['amount']
    assert factor.unit == payload['unit']


@pytest.mark.django_db
def test_add_factor_fails_when_recipe_ingredient_is_duplicated(client, ingredient, recipe):
    baker.make(Factor, recipe=recipe, ingredient=ingredient)
    payload = {'ingredient': ingredient.pk, 'amount': 0.5, 'unit': 'L'}
    with pytest.raises(IntegrityError) as err:
        client.post(f'/recipes/{recipe.pk}/add-factor/', payload)
    assert 'UNIQUE constraint failed' in str(err)


@pytest.mark.django_db
def test_add_factor_fails_when_recipe_does_not_exist(client):
    response = client.get('/recipes/1/add-factor/')
    assert response.status_code == HTTPStatus.NOT_FOUND
