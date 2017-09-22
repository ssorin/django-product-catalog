# -*- coding: utf-8 -*-
""" Product Catalog: Template tags """

from django import template
from django.db.models import Count

from ..models.category import Category
from ..models.product import Product

register = template.Library()


@register.inclusion_tag('product_catalog/tags/dummy.html', takes_context=True)
def get_categories(context, template='product_catalog/tags/categories.html'):
    """
    Return the published categories.
    """
    return {'template': template,
            'categories': Category.published.all().annotate(count_products_published=Count('products')),
            'context_category': context.get('category')}

@register.inclusion_tag('product_catalog/tags/dummy.html')
def get_last_products(number=5, template='product_catalog/tags/last_products.html'):
    """
    Return the most recent products.
    """
    return {'template': template,
            'products': Product.published.all()[:number]}
