# -*- coding: utf-8 -*-
""" Category model for Product Catalog """

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from mptt.managers import TreeManager
from mptt.models import MPTTModel
from mptt.models import TreeForeignKey

from product_catalog.managers import ProductsRelatedPublishedManager
from product_catalog.managers import product_published


@python_2_unicode_compatible
class Category(MPTTModel):
    """
    Simple model for categorizing products.
    """

    title = models.CharField(
        _('title'), max_length=255)

    slug = models.SlugField(
        _('slug'), unique=True, max_length=255, db_index=True,
        help_text=_("Used to build the category's URL."))

    description = models.TextField(
        _('description'), blank=True)

    parent = TreeForeignKey(
        'self',
        related_name='children',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('parent category'))

    objects = TreeManager()
    published = ProductsRelatedPublishedManager()

    @models.permalink
    def get_absolute_url(self):
        """
        Builds and returns the category's URL
        based on his tree path.
        """
        return 'product_catalog:category_detail', (self.slug,)

    def __str__(self):
        return self.title

    def product_published(self):
        """
        Returns category's published products.
        """
        return product_published(self.products)


    class Meta:
        """
        Category's meta information.
        """
        ordering = ['title']
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    class MPTTMeta:
        """
        Category MPTT's meta information.
        """
        order_insertion_by = ['title']
