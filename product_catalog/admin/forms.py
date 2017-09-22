# -*- coding: utf-8 -*-
""" Product Catalog: admin forms """

from django import forms
from mptt.forms import TreeNodeMultipleChoiceField
from product_catalog.models.category import Category


class CategoryAdminForm(forms.ModelForm):
    """
    Form for Category's Admin.
    Displays the level of hierarchy between parent / children
    """
    categories = TreeNodeMultipleChoiceField(
        level_indicator='---',
        required=False,
        queryset=Category.objects.all())
