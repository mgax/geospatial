from http import HTTPStatus

import pytest

from geospatial.content.models import HomePage
from geospatial.content.models import SimplePage

pytestmark = [pytest.mark.django_db]


def test_homepage(client):
    homepage = HomePage.objects.get()

    assert homepage.url == '/'
    response = client.get(homepage.url)
    assert response.status_code == HTTPStatus.OK
    html = response.content.decode('utf8')
    assert '<meta charset="utf-8"' in html


def test_simple_page(client):
    homepage = HomePage.objects.get()
    about = SimplePage(
        title='About',
        slug='about',
        body='<p>esome<em>Geography</em> is aw</p>',
    )
    homepage.add_child(instance=about)

    assert about.url == '/about/'
    response = client.get(about.url)
    assert response.status_code == HTTPStatus.OK
    html = response.content.decode('utf8')
    assert '<p>esome<em>Geography</em> is aw</p>' in html


def test_nav_bar(client):
    homepage = HomePage.objects.get()
    about = SimplePage(
        title='About',
        slug='about',
        show_in_menus=True,
    )
    homepage.add_child(instance=about)

    response = client.get(homepage.url)
    assert response.status_code == HTTPStatus.OK
    html = response.content.decode('utf8')
    assert '[<a href="/about/">About</a>]' in html
