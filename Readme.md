# CMS for geo-spatial.org website


## Content administration

The website is built using [Wagtail][]. Have a look at the [Wagtail Editor Manual][] for a nice overview of what's possible.

[Wagtail]: https://wagtail.io/
[Wagtail Editor Manual]: https://docs.wagtail.io/en/stable/editor_manual/index.html

To log into the admin section, go to `https://{site_domain}/admin/`, and log in with your email and password.


## Development

To create a local development environment:

```shell
cp example-docker.env docker.env
cp docker-compose.develop.yml docker-compose.override.yml
docker-compose build --pull
docker-compose up -d
docker-compose exec app ./manage.py migrate
docker-compose exec app ./manage.py createsuperuser
```

Then go to http://localhost:8000/admin/ and log in with the user you've just created.
