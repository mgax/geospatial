from django.db import models
from django.contrib.auth.models import AbstractUser

from wagtail.core.models import Page


class User(AbstractUser):
    pass


class HomePage(Page):
    pass
