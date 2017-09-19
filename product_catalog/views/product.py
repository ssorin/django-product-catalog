# -*- coding: utf-8 -*-
""" Product Catalog: Product view """
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from product_catalog.models.product import Product
from product_catalog.settings import PAGINATION


class ProductListView(ListView):
    """ """
    model = Product
    context_object_name = "product_list"
    paginate_by = PAGINATION

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        return context

class ProductDetailView(DetailView):
    """ """
    model = Product
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        return context
