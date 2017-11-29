# coding=utf-8
""" Product Catalog: models product_abstract test cases """

from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from product_catalog.models.product_abstract import AbstractProduct
from product_catalog.models import load_model_class


class LoadModelClassTestCase(TestCase):
    def test_load_model_class(self):
        self.assertEqual(
            load_model_class('product_catalog.models.product_abstract.AbstractProduct'),
            AbstractProduct)
        self.assertRaises(ImproperlyConfigured,
                          load_model_class, 'invalid.path.models.WrongModel')
