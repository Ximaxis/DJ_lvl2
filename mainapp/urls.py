from django.urls import re_path
from .views import *


urlpatterns = [
    re_path(r'^$', main, name='main'),

    re_path(r'^shop/(?P<slug>[-\w]+)/$', products, name='products'),
    re_path(r'^contacts/$', contacts, name='contacts'),
    re_path(r'^blog/blogsingle/$', blogsingle, name='blogsingle'),
    re_path(r'^blog/$', blog, name='blog'),
    re_path(r'^about$', about, name='about'),
    re_path(r'^shop/$', shop, name='shop'),
    re_path(r'^shop/category/(?P<slug>[-\w]+)/$', shop, name='category'),
    re_path(r'^shop/category/(?P<slug>[-\w]+)/page/(?P<page>\d+)/$', shop, name='page'),
    re_path(r'^checkout/$', checkout, name='checkout'),
]