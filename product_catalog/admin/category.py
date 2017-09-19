# -*- coding: utf-8 -*-

""" CategoryAdmin for Product Catalog """

from django.core.urlresolvers import NoReverseMatch
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from mptt.admin import MPTTModelAdmin, TreeRelatedFieldListFilter


class CategoryAdmin(MPTTModelAdmin):
    """
    Admin for Category model.
    """

    fields = ('title', 'parent', 'description', 'slug')
    list_display = ('title', 'slug', 'description', 'get_path')
    prepopulated_fields = {'slug': ('title', )}
    search_fields = ('title', 'description')
    list_filter = (('parent', TreeRelatedFieldListFilter),)
    mptt_level_indent = 20

    def __init__(self, model, admin_site):
        self.form.admin_site = admin_site
        super(CategoryAdmin, self).__init__(model, admin_site)

    def get_path(self, category):
        """
        Return the category's tree path in HTML.
        """
        try:
            return format_html(
                '<a href="{}" target="blank">{}</a>',
                category.get_absolute_url(), category.get_absolute_url())
        except NoReverseMatch:
            return '/%s/' % category.slug
    get_path.short_description = _('Display on website')

