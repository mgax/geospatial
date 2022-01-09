from http import HTTPStatus

import pytest

from geospatial.content.models import HomePage
from geospatial.content.models import AuthorIndexPage
from geospatial.content.models import AuthorPage

pytestmark = [pytest.mark.django_db]


def test_author_index_page(client):
    homepage = HomePage.objects.get()
    author_index = AuthorIndexPage(
        title='Authors',
        slug='authors',
    )
    homepage.add_child(instance=author_index)
    author = AuthorPage(
        title='Mr Fancy Pants',
        slug='mr-fancy-pants',
        intro='a short abstract',
    )
    author_index.add_child(instance=author)

    assert author_index.url == '/authors/'
    response = client.get(author_index.url)
    assert response.status_code == HTTPStatus.OK
    html = response.content.decode('utf8')
    assert author.title in html
    assert f'href="{author.url}"' in html
    assert author.intro in html


def test_author_page(client):
    homepage = HomePage.objects.get()
    author_index = AuthorIndexPage(
        title='Authors',
        slug='authors',
    )
    homepage.add_child(instance=author_index)
    author = AuthorPage(
        title='Mr Fancy Pants',
        slug='mr-fancy-pants',
        intro='a short abstract',
    )
    author_index.add_child(instance=author)

    assert author.url == '/authors/mr-fancy-pants/'
    response = client.get(author.url)
    html = response.content.decode('utf8')
    assert author.title in html
    assert author.intro in html
