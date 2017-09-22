# -*- coding: utf-8 -*-
""" Product Catalog: Product view """

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from product_catalog.models.product import Product
from product_catalog.settings import PAGINATION


class ProductListView(ListView):
    """ """
    context_object_name = "product_list"
    paginate_by = PAGINATION

    def get_queryset(self, **kwargs):
        return Product.published.all()


class ProductDetailView(DetailView):
    """ """
    context_object_name = "product"

    def get_queryset(self, **kwargs):
        return Product.published.all()
