from http import HTTPStatus

import pytest

from geospatial.content.models import HomePage
from geospatial.content.models import AuthorIndexPage
from geospatial.content.models import AuthorPage
from geospatial.content.models import ArticleIndexPage
from geospatial.content.models import ArticlePage

pytestmark = [pytest.mark.django_db]


def test_article_index_page(client):
    homepage = HomePage.objects.get()
    article_index = ArticleIndexPage(
        title='Articles',
        slug='articles',
    )
    homepage.add_child(instance=article_index)
    article = ArticlePage(
        title='My Fancy Paper',
        slug='my-fancy-paper',
        intro='a short abstract',
        body='a whole lot of text here'
    )
    article_index.add_child(instance=article)

    assert article_index.url == '/articles/'
    response = client.get(article_index.url)
    assert response.status_code == HTTPStatus.OK
    html = response.content.decode('utf8')
    assert article.title in html
    assert f'href="{article.url}"' in html
    assert article.intro in html
    assert article.body not in html


def test_article_page(client):
    homepage = HomePage.objects.get()
    article_index = ArticleIndexPage(
        title='Articles',
        slug='articles',
    )
    homepage.add_child(instance=article_index)
    article = ArticlePage(
        title='My Fancy Paper',
        slug='my-fancy-paper',
        intro='a short abstract',
        body='a whole lot of text here'
    )
    article_index.add_child(instance=article)

    assert article.url == '/articles/my-fancy-paper/'
    response = client.get(article.url)
    html = response.content.decode('utf8')
    assert article.title in html
    assert article.intro in html
    assert article.body in html


def test_article_authors(client):
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

    article_index = ArticleIndexPage(
        title='Articles',
        slug='articles',
    )
    homepage.add_child(instance=article_index)
    article = ArticlePage(
        title='My Fancy Paper',
        slug='my-fancy-paper',
        authors=[author],
        intro='a short abstract',
        body='a whole lot of text here'
    )
    article_index.add_child(instance=article)

    article_response = client.get(article.url)
    assert article_response.status_code == HTTPStatus.OK
    article_html = article_response.content.decode('utf8')
    assert author.title in article_html
    assert author.url in article_html

    article_index_response = client.get(article_index.url)
    assert article_index_response.status_code == HTTPStatus.OK
    article_index_html = article_index_response.content.decode('utf8')
    assert author.title in article_index_html
    assert author.url in article_index_html
