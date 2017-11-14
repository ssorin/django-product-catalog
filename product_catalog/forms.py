# -*- coding: utf-8 -*-
""" Product Catalog: forms """

from django import forms
from mptt.forms import TreeNodeMultipleChoiceField
from product_catalog.models.category import Category
from product_catalog.models.product import Product

from product_catalog.settings import FORM_UPDATE_FIELDS, FORM_CREATE_FIELDS



class CategoryForm(forms.ModelForm):
    """
    Form for Category's
    Displays the level of hierarchy between parent / children
    """
    categories = TreeNodeMultipleChoiceField(
        level_indicator='---',
        required=False,
        queryset=Category.objects.all())

class CategoryUpdateForm(CategoryForm):
    class Meta:
        model = Product
        fields = FORM_UPDATE_FIELDS

class CategoryCreateForm(CategoryForm):
    class Meta:
        model = Product
        fields = FORM_CREATE_FIELDS
