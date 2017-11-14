# -*- coding: utf-8 -*-
""" Product Catalog: Product view """

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from product_catalog.models.product import Product
from product_catalog.settings import PAGINATION
from product_catalog.views.mixins.auth_mixins import FrontManagementIsOpenMixin, AccessMixin, CreateAccessMixin

from product_catalog.forms import CategoryUpdateForm, CategoryCreateForm

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


class ProductCreateView(FrontManagementIsOpenMixin, CreateAccessMixin, CreateView):
    """ """
    model = Product
    form_class = CategoryCreateForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(ProductCreateView, self).form_valid(form)


class ProductUpdateView(FrontManagementIsOpenMixin, AccessMixin, UpdateView):
    """ """
    model = Product
    form_class = CategoryUpdateForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(ProductUpdateView, self).form_valid(form)


class ProductDeleteView(FrontManagementIsOpenMixin, AccessMixin, DeleteView):
    """ """
    model = Product
    success_url = reverse_lazy('product_catalog:product_list')
