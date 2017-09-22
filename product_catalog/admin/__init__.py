# -*- coding: utf-8 -*-
""" Product Catalog: Admin """

from django.contrib import admin

from product_catalog.admin.category import CategoryAdmin
from product_catalog.models.category import Category
from product_catalog.admin.product import ProductAdmin
from product_catalog.models.product import Product

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
