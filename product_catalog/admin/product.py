# # -*- coding: utf-8 -*-
""" ProductAdmin for Product Catalog """

from django.contrib import admin
from django.core.urlresolvers import NoReverseMatch
from django.utils.html import conditional_escape
from django.utils.html import format_html_join, format_html
from django.utils.translation import ugettext_lazy as _

from product_catalog.admin.forms import CategoryAdminForm

class ProductAdmin(admin.ModelAdmin):
    """
    Admin for Product model.
    """
    form = CategoryAdminForm

    fieldsets = (
        (_('Content'), {
            'fields': (('title', 'status'), 'slug', 'excerpt', 'content', 'categories')}),
        (_('Illustration'), {
            'fields': ('image', 'get_thumbnail', 'image_caption'),
            'classes': ('collapse', 'collapse-closed')}),
        (_('Publication'), {
            'fields': ('start_publication', 'end_publication'),
            'classes': ('collapse', 'collapse-closed')}),
        (None, {'fields': ('creation_date', 'last_update', 'owner')})
    )
    readonly_fields = ['slug', 'get_thumbnail', 'creation_date', 'last_update']
    list_filter = ('status',)
    list_display = ('title', 'get_categories', 'get_is_visible', 'get_thumbnail')
    actions_on_top = True

    def __init__(self, model, admin_site):
        self.form.admin_site = admin_site
        super(ProductAdmin, self).__init__(model, admin_site)

    def save_related(self, request, form, formsets, change):
        """
        Add all parents of the selected category
        """
        super(ProductAdmin, self).save_related(request, form, formsets, change)
        for category in form.instance.categories.all():
            parent = category.parent
            while parent is not None:
                form.instance.categories.add(parent)
                parent = parent.parent

    def get_categories(self, product):
        """
        Return the categories.
        """
        try:
            return format_html_join(
                ', ', u'<a href="{}" target="blank">{}</a>',
                [(category.get_absolute_url(), category.title)
                 for category in product.categories.all()])
        except NoReverseMatch:
            return ', '.join([conditional_escape(category.title) for category in product.categories.all()])
    get_categories.short_description = _('category(s)')

    def get_is_visible(self, product):
        """
        Admin wrapper for product.is_visible.
        """
        return product.is_visible
    get_is_visible.boolean = True
    get_is_visible.short_description = _('is visible')

    def get_thumbnail(self, product):
        """
        Admin wrapper to display product.image as thumbnail.
        """
        if product.image:
            return format_html('<a href="%s" target="_blank"><img src="%s" width=80/></a>'
                               % (product.image.url, product.image.url))
        return None
    get_thumbnail.short_description = _('thumbnail')
