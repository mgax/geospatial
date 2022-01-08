from django.urls import include
from django.urls import path
import django.contrib.admin
import wagtail.admin.urls
import wagtail.core.urls
import wagtail.documents.urls

import geospatial.search.views

urlpatterns = [
    path('django-admin/', django.contrib.admin.site.urls),
    path('admin/', include(wagtail.admin.urls)),
    path('documents/', include(wagtail.documents.urls)),
    path('search/', geospatial.search.views.search, name='search'),
    path('', include(wagtail.core.urls)),
]
