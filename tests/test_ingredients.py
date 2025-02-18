from http import HTTPStatus

import pytest
from model_bakery import baker
from pytest_django.asserts import assertContains, assertRedirects

from ingredients.models import Ingredient


@pytest.mark.django_db
def test_ingredient_list_is_properly_displayed(client):
    ingredients = baker.make(Ingredient, _fill_optional=True, _quantity=10)
    response = client.get('/ingredients/')
    for ingredient in ingredients:
        assertContains(response, ingredient.name)


@pytest.mark.django_db
def test_proper_message_is_shown_when_ingredient_list_is_empty(client):
    response = client.get('/ingredients/')
    assertContains(response, 'No ingredients so far!')


@pytest.mark.django_db
def test_ingredient_list_contains_links_to_ingredient_detail(client):
    ingredients = baker.make(Ingredient, _fill_optional=True, _quantity=10)
    response = client.get('/ingredients/')
    for ingredient in ingredients:
        href = f'href="/ingredients/{ingredient.pk}/"'
        assertContains(response, href)


@pytest.mark.django_db
def test_ingredient_list_contains_link_to_add_ingredient(client):
    response = client.get('/ingredients/')
    assertContains(response, 'href="/ingredients/add/"')


@pytest.mark.django_db
def test_add_ingredient_form_contains_proper_fields(client):
    response = client.get('/ingredients/add/')
    assertContains(response, 'Name:')
    assertContains(response, 'Description:')


@pytest.mark.django_db
def test_add_ingredient_works_properly(client, fake):
    payload = {'name': fake.name(), 'description': fake.paragraph()}
    response = client.post('/ingredients/add/', payload)
    assertRedirects(response, '/ingredients/')
    ingredient = Ingredient.objects.get(name=payload['name'])
    assert ingredient.description == payload['description']


@pytest.mark.django_db
def test_add_ingredient_fails_when_name_is_duplicated(client, fake, ingredient):
    payload = {'name': ingredient.name, 'description': fake.paragraph()}
    response = client.post('/ingredients/add/', payload)
    assertContains(response, 'Ingredient with this Name already exists')


@pytest.mark.django_db
def test_ingredient_detail_contains_proper_content(client, ingredient):
    response = client.get(f'/ingredients/{ingredient.pk}/')
    assertContains(response, ingredient.name)
    assertContains(response, ingredient.description)


@pytest.mark.django_db
def test_ingredient_detail_shows_proper_message_when_no_description_exists(client, ingredient):
    ingredient.description = ''
    ingredient.save()
    response = client.get(f'/ingredients/{ingredient.pk}/')
    assertContains(response, ingredient.name)
    assertContains(response, 'No description so far!')


@pytest.mark.django_db
def test_ingredient_detail_returns_404_when_ingredient_does_not_exist(client):
    response = client.get('/ingredients/1/')
    assert response.status_code == HTTPStatus.NOT_FOUND
