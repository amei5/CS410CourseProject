from django.urls import path
from django.urls import re_path as url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^get_search_summary/$', views.get_search_summary, name='get_search_summary'),
]