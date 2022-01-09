from http import HTTPStatus

import pytest

pytestmark = [pytest.mark.django_db]


def test_homepage(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    html = response.content.decode('utf8')
    assert '<meta charset="utf-8"' in html
