from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms
from modelcluster.fields import ParentalKey
from modelcluster.fields import ParentalManyToManyField
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.admin.edit_handlers import InlinePanel
from wagtail.search import index
from wagtail.images.edit_handlers import ImageChooserPanel


class User(AbstractUser):
    pass


class HomePage(Page):
    parent_page_types = []

    @property
    def nav_pages(self):
        return self.get_children().live().in_menu()

    @property
    def recent_published_articles(self):
        return ArticlePage.objects.descendant_of(self).live()


class SimplePage(Page):
    body = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('body', classname='full'),
    ]


class AuthorIndexPage(Page):
    subpage_types = [
        'content.AuthorPage',
    ]

    @property
    def published_authors(self):
        return self.get_children().live()


class AuthorPage(Page):
    intro = models.CharField(max_length=4000)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        InlinePanel('photos', label='Photos'),
    ]

    parent_page_types = [
        'content.AuthorIndexPage',
    ]

    @property
    def published_articles(self):
        return self.articlepage_set.live()


class AuthorPhoto(models.Model):
    page = ParentalKey(
        AuthorPage, on_delete=models.CASCADE, related_name='photos'
    )
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )

    panels = [
        ImageChooserPanel('image'),
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
    authors = ParentalManyToManyField(AuthorPage, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('authors', widget=forms.CheckboxSelectMultiple),
        FieldPanel('intro'),
        FieldPanel('body', classname='full'),
    ]

    parent_page_types = [
        'content.ArticleIndexPage',
    ]
