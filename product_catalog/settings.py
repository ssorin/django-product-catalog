# -*- coding: utf-8 -*-
""" Product Catalog: Settings """

from django.conf import settings


PAGINATION = getattr(settings, 'PRODUCT_CATALOG_PAGINATION', 10)

PRODUCT_BASE_MODEL = getattr(settings, 'PRODUCT_CATALOG_PRODUCT_BASE_MODEL',
                             'product_catalog.models.product_abstract.AbstractProduct')

UPLOAD_TO = getattr(settings, 'PRODUCT_CATALOG_UPLOAD_TO', 'uploads/product_catalog/%Y/%m/%d/')

# Add / Update / Delete on front settings
FRONT_MANAGEMENT = getattr(settings, 'PRODUCT_CATALOG_FRONT_MANAGEMENT', True)

PERMISSION_OPTIONS_SUPERUSER = getattr(settings, 'PRODUCT_CATALOG_PERMISSION_OPTIONS_SUPERUSER', 0)
PERMISSION_OPTIONS_STAFF = getattr(settings, 'PRODUCT_CATALOG_PERMISSION_OPTIONS_STAFF', 1)
PERMISSION_OPTIONS_OWNER = getattr(settings, 'PRODUCT_CATALOG_PERMISSION_OPTIONS_OWNER', 2)

# if PERMISSION_OPTIONS_OWNER is chosen, all user will be able to create a new product in front
ACCESS_PERMISSION = getattr(settings, 'PRODUCT_CATALOG_ACCESS_PERMISSION', PERMISSION_OPTIONS_OWNER)


FORM_FIELDS = getattr(
    settings,
    'PRODUCT_CATALOG_FORM_FIELDS',
    ['title', 'status', 'excerpt', 'content', 'categories', 'image']
)
FORM_UPDATE_FIELDS = getattr(settings, 'PRODUCT_CATALOG_FORM_UPDATE_FIELDS', FORM_FIELDS)
FORM_CREATE_FIELDS = getattr(settings, 'PRODUCT_CATALOG_FORM_CREATE_FIELDS', FORM_FIELDS)


