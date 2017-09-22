# -*- coding: utf-8 -*-
""" Product Catalog: Settings """

from django.conf import settings


PAGINATION = getattr(settings, 'PRODUCT_CATALOG_PAGINATION', 2)

PRODUCT_BASE_MODEL = getattr(settings, 'PRODUCT_CATALOG_PRODUCT_BASE_MODEL',
                             'product_catalog.models.product_abstract.AbstractProduct')

UPLOAD_TO = getattr(settings, 'PRODUCT_CATALOG_UPLOAD_TO', 'uploads/product_catalog/%Y/%m/%d/')
