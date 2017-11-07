# -*- coding: utf-8 -*-
""" Product Catalog: Product view """

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from product_catalog.models.product import Product
from product_catalog.settings import PAGINATION, FORM_UPDATE_FIELDS, FORM_CREATE_FIELDS
from product_catalog.views.mixins.auth_mixins import AccessMixin

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

# TODO: Add verif settings.PRODUCT_CATALOG_FRONT_MANAGEMENT to access this view
class ProductCreateView(LoginRequiredMixin, CreateView):
    """ """
    model = Product
    fields = FORM_CREATE_FIELDS

    def form_valid(self, form):
        owner = self.request.user
        form.instance.owner = owner
        return super(ProductCreateView, self).form_valid(form)

# TODO: Add verif settings.PRODUCT_CATALOG_FRONT_MANAGEMENT to access this view
class ProductUpdateView(AccessMixin, UpdateView):
    """ """
    model = Product
    fields = FORM_UPDATE_FIELDS

    def form_valid(self, form):
        owner = self.request.user
        form.instance.owner = owner
        return super(ProductUpdateView, self).form_valid(form)

# TODO: Add verif settings.PRODUCT_CATALOG_FRONT_MANAGEMENT to access this view
class ProductDeleteView(AccessMixin, DeleteView):
    """ """
    model = Product
    success_url = reverse_lazy('product_catalog:product_list')
