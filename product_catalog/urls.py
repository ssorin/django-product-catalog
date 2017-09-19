# -*- coding: utf-8 -*-
""" Product Catalog: Defaults urls """

from django.conf.urls import include
from django.conf.urls import url

from product_catalog.views.category import CategoryListView, CategoryDetailView
from product_catalog.views.product import ProductListView, ProductDetailView

app_name = 'product_catalog'

urlpatterns = [
    # Category
    url(r'^categories/$', CategoryListView.as_view(), name='category_list'),
    url(
        r'^categories/(?P<slug>[-\w]+)/page/(?P<page>\d+)/$',
        CategoryDetailView.as_view(),
        name='category_detail_paginated'
        ),
    url(r'^categories/(?P<slug>[-\w]+)/$', CategoryDetailView.as_view(), name='category_detail'),

    # Product
    url(r'^products/$', ProductListView.as_view(), name='product_list'),
    url(r'^products/(?P<slug>[-\w]+)/$', ProductDetailView.as_view(), name='product_detail'),

    # Home
    url(r'^$', ProductListView.as_view(), name='product_home'),
]
