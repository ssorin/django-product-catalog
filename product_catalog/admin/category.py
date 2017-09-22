# -*- coding: utf-8 -*-

""" Product Catalog: CategoryAdmin """

from django.core.urlresolvers import NoReverseMatch
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from mptt.admin import MPTTModelAdmin, TreeRelatedFieldListFilter


class CategoryAdmin(MPTTModelAdmin):
    """
    Admin for Category model.
    """

    fields = ('title', 'parent', 'description', 'slug')
    list_display = ('title', 'description', 'get_view_on_site')
    prepopulated_fields = {'slug': ('title', )}
    search_fields = ('title', 'description')
    list_filter = (('parent', TreeRelatedFieldListFilter),)
    view_on_site = True
    mptt_level_indent = 20

    def __init__(self, model, admin_site):
        self.form.admin_site = admin_site
        super(CategoryAdmin, self).__init__(model, admin_site)

    def get_view_on_site(self, category):
        """
        Return the category's tree path in HTML.
        """
        try:
            url = category.get_absolute_url()
            return format_html('<a href="%s" target="blank">%s</a>' % (url, url))
        except NoReverseMatch:
            return '/%s/' % category.slug
    get_view_on_site.short_description = _('View on site')

