from http import HTTPStatus

import pytest

from geospatial.content.models import HomePage
from geospatial.content.models import SimplePage

pytestmark = [pytest.mark.django_db]


def test_homepage(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    html = response.content.decode('utf8')
    assert '<meta charset="utf-8"' in html


def test_simple_page(client):
    home = HomePage.objects.get()
    about = SimplePage(
        title='About',
        slug='about',
        body='<p>esome<em>Geography</em> is aw</p>',
    )
    home.add_child(instance=about)

    response = client.get(about.url)
    assert response.status_code == HTTPStatus.OK
    html = response.content.decode('utf8')
    assert '<p>esome<em>Geography</em> is aw</p>' in html


def test_nav_bar(client):
    home = HomePage.objects.get()
    about = SimplePage(
        title='About',
        slug='about',
        show_in_menus=True,
    )
    home.add_child(instance=about)
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    html = response.content.decode('utf8')
    assert '[<a href="/about/">About</a>]' in html
