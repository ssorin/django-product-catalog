# -*- coding: utf-8 -*-
""" Product Catalog: Defaults urls """

from django.conf.urls import url
from django.views.generic import TemplateView

from product_catalog.views.category import CategoryListView, CategoryDetailView
from product_catalog.views.product import ProductListView, ProductDetailView, ProductCreateView, \
    ProductUpdateView, ProductDeleteView
from product_catalog.settings import FRONT_MANAGEMENT

app_name = 'product_catalog'

urlpatterns = []
if FRONT_MANAGEMENT:
    urlpatterns += [
        url(r'^products/add/$', ProductCreateView.as_view(), name='product_add'),
        url(r'^products/update/(?P<pk>[0-9]+)/$', ProductUpdateView.as_view(), name='product_update'),
        url(r'^products/delete/(?P<pk>[0-9]+)/$', ProductDeleteView.as_view(), name='product_delete'),
    ]

urlpatterns += [
    # Category
    url(r'^categories/$', CategoryListView.as_view(), name='category_list'),
    url(r'^categories/(?P<slug>[-\w]+)/$', CategoryDetailView.as_view(), name='category_detail'),

    # Product
    url(r'^products/$', ProductListView.as_view(), name='product_list'),
    url(r'^products/(?P<slug>[-\w]+)/$', ProductDetailView.as_view(), name='product_detail'),

    # Home
    url(r'^$', TemplateView.as_view(template_name='product_catalog/home.html'), name='product_home'),
]
