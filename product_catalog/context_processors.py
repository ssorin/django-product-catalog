# -*- coding: utf-8 -*-
""" Product Catalog: Context processor """

from product_catalog.settings import FRONT_MANAGEMENT

def product_front_management(request):
    """
        Access to settings.FRONT_MANAGEMENT & settings.FRONT_MANAGEMENT
    """

    return {
        'FRONT_MANAGEMENT': FRONT_MANAGEMENT
    }