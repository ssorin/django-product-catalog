# # -*- coding: utf-8 -*-
# """ ProductAdmin for Product Catalog """

from django.contrib import admin
from django.core.urlresolvers import NoReverseMatch
from django.utils.html import conditional_escape
from django.utils.html import format_html_join
from django.utils.translation import ugettext_lazy as _

from product_catalog.admin.forms import CategoryAdminForm

class ProductAdmin(admin.ModelAdmin):
    """
    Admin for Entry model.
    """
    form = CategoryAdminForm

    fieldsets = (
        (_('Content'), {
            'fields': (('title', 'status'), 'excerpt', 'content', 'categories')}),
        (_('Illustration'), {
            'fields': ('image', 'image_caption'),
            'classes': ('collapse', 'collapse-closed')}),
        (_('Publication'), {
            'fields': ('start_publication', 'end_publication'),
            'classes': ('collapse', 'collapse-closed')})
    )

    list_filter = ('status',)
    list_display = ('title', 'get_categories', 'get_is_visible', )

    actions = ['make_published', 'make_hidden',]
    actions_on_top = True
    actions_on_bottom = True

    def __init__(self, model, admin_site):
        self.form.admin_site = admin_site
        super(ProductAdmin, self).__init__(model, admin_site)

    def get_categories(self, entry):
        """
        Return the categories linked in HTML.
        """
        try:
            return format_html_join(
                ', ', '<a href="{}" target="blank">{}</a>',
                [(category.get_absolute_url(), category.title)
                 for category in entry.categories.all()])
        except NoReverseMatch:
            return ', '.join([conditional_escape(category.title)
                              for category in entry.categories.all()])
    get_categories.short_description = _('category(s)')

    def get_is_visible(self, product):
        """
        Admin wrapper for product.is_visible.
        """
        return product.is_visible
    get_is_visible.boolean = True
    get_is_visible.short_description = _('is visible')

    # Custom Methods
    def get_actions(self, request):
        """
        Define actions by user's permissions.
        """
        actions = super(ProductAdmin, self).get_actions(request)
        if not actions:
            return actions

        if not request.user.has_perm('zinnia.can_change_status'):
            del actions['make_hidden']
            del actions['make_published']

        return actions
