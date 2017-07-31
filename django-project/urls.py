from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'', include('OGvis.urls')),
    url(r'^$', views.index, name='index'),
]
