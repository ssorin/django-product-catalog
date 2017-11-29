# coding=utf-8
""" Product Catalog: models Category test cases """

from django.test import TestCase

from product_catalog.models.product import Product
from product_catalog.models.category import Category


class CategoryTestCase(TestCase):

    def setUp(self):
        self.categories = [
            Category.objects.create(title='Category 1',
                                    slug='category-1'),
            Category.objects.create(title='Category 2',
                                    slug='category-2')
        ]

        params = {'title': 'Product 1',
                  'content': 'Lorem ipsum',
                  'slug': 'product-1'}
        self.product = Product.objects.create(**params)

    # get_absolute_url

    def test_product_published(self):
        category = self.categories[0]
        self.assertEqual(category.product_published().count(), 0)

        self.product.categories.add(*self.categories)
        self.product.save()
        self.assertEqual(category.product_published().count(), 1)

        params = {'title': 'Product 2',
                  'content': 'Lorem ipsum 2',
                  'slug': 'product-2'}

        product2 = Product.objects.create(**params)
        product2.categories.add(self.categories[0])

        self.assertEqual(self.categories[0].product_published().count(), 2)
        self.assertEqual(self.categories[1].product_published().count(), 1)

    def test_get_absolute_url(self):
        self.assertEqual('/categories/category-1/', self.categories[0].get_absolute_url())
