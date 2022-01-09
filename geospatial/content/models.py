from django.db import models
from django.contrib.auth.models import AbstractUser

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.search import index


class User(AbstractUser):
    pass


class HomePage(Page):
    parent_page_types = []

    @property
    def nav_pages(self):
        return self.get_children().live().in_menu()


class SimplePage(Page):
    body = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('body', classname='full'),
    ]


class ArticleIndexPage(Page):
    subpage_types = [
        'content.ArticlePage',
    ]

    @property
    def published_articles(self):
        return self.get_children().live()


class ArticlePage(Page):
    intro = models.CharField(max_length=4000)
    body = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('body', classname='full'),
    ]

    parent_page_types = [
        'content.ArticleIndexPage',
    ]
