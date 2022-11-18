from django.urls import path
from django.urls import re_path as url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^get_ebay_summary/$', views.get_ebay_summary, name='get_ebay_summary'),
]