# -*- coding: utf-8 -*-
""" Product Catalog: Product model """

from product_catalog.models import load_model_class
from product_catalog.settings import PRODUCT_BASE_MODEL


class Product(load_model_class(PRODUCT_BASE_MODEL)):
    """
    The final Product model based on inheritance.
    """
