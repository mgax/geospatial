# CMS pentru site-ul geo-spatial.org


## Administrarea de conținut

Site-ul este construit cu [Wagtail][]. Consultați și [Manualul Wagtail pentru editori][].

[Wagtail]: https://wagtail.io/
[Manualul Wagtail pentru editori]: https://docs.wagtail.io/en/stable/editor_manual/index.html

Pentru login în zona de administrare, mergeți la `https://{site_domain}/admin/`, și autentificați-vă cu username și parolă.


## Development

Codul sursă și mesajele de commit sunt în limba engleză.

Pentru a instala aplicația local:

```shell
cp example-docker.env docker.env
cp docker-compose.develop.yml docker-compose.override.yml
docker-compose build --pull
docker-compose up -d
docker-compose exec app ./manage.py collectstatic
docker-compose exec app ./manage.py migrate
docker-compose exec app ./manage.py createsuperuser
```

Mergeți la http://localhost:8000/admin/ și autentificați-vă cu userul creat mai sus.

### Rulat testele

```shell
docker-compose exec app pytest
```
