from http import HTTPStatus

import pytest
import datetime

from geospatial.content.models import HomePage
from geospatial.content.models import AuthorIndexPage
from geospatial.content.models import AuthorPage
from geospatial.content.models import EventIndexPage
from geospatial.content.models import EventPage

pytestmark = [pytest.mark.django_db]


def test_event_index_page(client):
    homepage = HomePage.objects.get()
    event_index = EventIndexPage(
        title='Events',
        slug='events',
    )
    homepage.add_child(instance=event_index)
    event = EventPage(
        title='My Fancy Event',
        slug='my-fancy-event',
        intro='a short abstract',
        body='a whole lot of text here',
        date=datetime.date.today() + datetime.timedelta(days=1)
    )
    event_index.add_child(instance=event)

    assert event_index.url == '/events/'
    response = client.get(event_index.url)
    assert response.status_code == HTTPStatus.OK
    html = response.content.decode('utf8')
    assert event.title in html
    assert f'href="{event.url}"' in html
    assert event.intro in html
    assert event.body not in html


def test_event_page(client):
    homepage = HomePage.objects.get()
    event_index = EventIndexPage(
        title='Events',
        slug='events',
    )
    homepage.add_child(instance=event_index)
    event = EventPage(
        title='My Fancy Event',
        slug='my-fancy-event',
        intro='a short abstract',
        body='a whole lot of text here',
        date=datetime.date.today() + datetime.timedelta(days=1)
    )
    event_index.add_child(instance=event)

    assert event.url == '/events/my-fancy-event/'
    response = client.get(event.url)
    html = response.content.decode('utf8')
    assert event.title in html
    assert event.intro in html
    assert event.body in html
    assert event.date in html


def test_event_authors(client):
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

    event_index = EventIndexPage(
        title='Events',
        slug='events',
    )
    homepage.add_child(instance=event_index)
    event = EventPage(
        title='My Fancy Event',
        slug='my-fancy-event',
        authors=[author],
        intro='a short abstract',
        body='a whole lot of text here',
        date=datetime.date.today() + datetime.timedelta(days=1)
    )
    event_index.add_child(instance=event)

    event_response = client.get(event.url)
    assert event_response.status_code == HTTPStatus.OK
    event_html = event_response.content.decode('utf8')
    assert author.title in event_html
    assert author.url in event_html

    event_index_response = client.get(event_index.url)
    assert event_index_response.status_code == HTTPStatus.OK
    event_index_html = event_index_response.content.decode('utf8')
    assert author.title in event_index_html
    assert author.url in event_index_html
