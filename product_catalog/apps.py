# -*- coding: utf-8 -*-
""" Product Catalog: Apps """

from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ProductCatalogConfig(AppConfig):
    """
    Config for Product Catalog application.
    """
    name = 'product_catalog'
    label = 'product_catalog'
    verbose_name = _('Product Catalog')
