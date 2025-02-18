import pytest
from django.conf import settings

from ingredients.models import Ingredient
from recipes.models import Factor, Recipe


@pytest.mark.django_db
def test_required_apps_are_installed():
    PROPER_APPS = ('shared', 'ingredients', 'recipes')

    custom_apps = [app for app in settings.INSTALLED_APPS if not app.startswith('django')]
    for app in PROPER_APPS:
        app_config = f'{app}.apps.{app.title()}Config'
        assert (
            app_config in custom_apps
        ), f'La aplicación <{app}> no está "creada/instalada" en el proyecto.'
    assert len(custom_apps) >= len(
        PROPER_APPS
    ), 'El número de aplicaciones propias definidas en el proyecto no es correcto.'


@pytest.mark.django_db
def test_models_has_proper_fields():
    MODEL_FIELDS = (
        (Recipe, ('id', 'name', 'script', 'ingredients')),
        (Factor, ('id', 'recipe', 'ingredient', 'amount', 'unit')),
        (Ingredient, ('id', 'name', 'description')),
    )
    for model, expected_fields in MODEL_FIELDS:
        for field in expected_fields:
            assert (
                getattr(model, field) is not None
            ), f'El campo <{field}> no está en el modelo {model.__name__}.'


@pytest.mark.django_db
def test_unit_field_from_factor_has_proper_choices():
    assert set(Factor.unit.field.choices) == {('G', 'Gram'), ('L', 'Liter'), ('P', 'Piece')}


@pytest.mark.django_db
def test_models_are_available_on_admin(admin_client):
    MODELS = (
        'recipes.Recipe',
        'recipes.Factor',
        'ingredients.Ingredient',
    )

    for model in MODELS:
        url_model_path = model.replace('.', '/').lower()
        url = f'/admin/{url_model_path}/'
        response = admin_client.get(url)
        assert response.status_code == 200, f'El modelo <{model}> no está habilitado en el admin.'
