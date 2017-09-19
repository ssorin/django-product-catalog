# -*- coding: utf-8 -*-
""" Product Catalog: Category view """

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from product_catalog.models.category import Category
from product_catalog.settings import PAGINATION


class CategoryListView(ListView):
    """ """
    model = Category
    context_object_name = "category_list"
    paginate_by = PAGINATION

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        return context

class CategoryDetailView(DetailView):
    """ """
    model = Category
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        return context
