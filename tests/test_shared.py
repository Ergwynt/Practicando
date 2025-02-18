import pytest
from pytest_django.asserts import assertContains


@pytest.mark.django_db
def test_root_page_contains_proper_links(client):
    response = client.get('/')
    assertContains(response, 'href="/ingredients/"')
    assertContains(response, 'href="/recipes/"')
