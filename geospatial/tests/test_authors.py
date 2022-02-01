from http import HTTPStatus
from io import BytesIO
import re

import pytest
from django.core.files.images import ImageFile
from wagtail.images.models import Image
import PIL.Image

from geospatial.content.models import HomePage
from geospatial.content.models import AuthorIndexPage
from geospatial.content.models import AuthorPage
from geospatial.content.models import ArticleIndexPage
from geospatial.content.models import ArticlePage
from geospatial.content.models import AuthorPhoto

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


def test_author_page_lists_articles(client):
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

    response = client.get(author.url)
    html = response.content.decode('utf8')
    assert author.title in html
    assert author.intro in html
    assert article.title in html
    assert article.url in html
    assert article.intro in html


def test_author_photo(client, settings, tmp_path):
    homepage = HomePage.objects.get()
    author_index = AuthorIndexPage(
        title='Authors',
        slug='authors',
    )
    homepage.add_child(instance=author_index)

    media_root = tmp_path / 'media'
    settings.MEDIA_ROOT = media_root
    f = BytesIO()
    image = PIL.Image.new('RGBA', (640, 480), 'cyan')
    image.save(f, 'PNG')
    portrait = Image.objects.create(
        title='Portrait',
        file=ImageFile(f, name='portrait.png'),
    )
    author = AuthorPage(
        title='Mr Fancy Pants',
        slug='mr-fancy-pants',
        intro='a short abstract',
        photos=[AuthorPhoto(image=portrait)],
    )
    author_index.add_child(instance=author)

    response = client.get(author.url)
    assert response.status_code == HTTPStatus.OK
    html = response.content.decode('utf8')
    m = re.search(r'<img [^>]*src="([^"]+)"[^>]*>', html)
    assert m is not None
    url = m.group(1)
    assert url.startswith(settings.MEDIA_URL)
    relarive_url = url[len(settings.MEDIA_URL):]
    assert not relarive_url.startswith('/')
    image_path = media_root / relarive_url
    assert image_path.exists()
