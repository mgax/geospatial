FROM python:3.8.1-slim-buster

WORKDIR /app
RUN useradd -m wagtail
EXPOSE 8000
ENV PYTHONUNBUFFERED=1 \
    PORT=8000

RUN apt-get update --yes --quiet \
 && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadbclient-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

COPY requirements requirements
RUN pip install -r requirements/base.txt -r requirements/dev.txt

RUN chown wagtail:wagtail /app
COPY --chown=wagtail:wagtail . .

USER wagtail
RUN ./manage.py collectstatic --noinput --clear

CMD ./run.sh prodserver
