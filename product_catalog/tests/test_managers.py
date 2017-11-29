# coding=utf-8
""" Product Catalog: managers test cases """

from pytz import UTC
from datetime import datetime

from django.test import TestCase

from product_catalog.models.product import Product
from product_catalog.models.category import Category
from product_catalog.managers import PUBLISHED, DRAFT, HIDDEN
from product_catalog.managers import product_published, ProductPublishedManager, ProductsRelatedPublishedManager


class ManagersTestCase(TestCase):

    def setUp(self):

        self.categories = [
            Category.objects.create(title='Category 1',
                                    slug='category-1'),
            Category.objects.create(title='Category 2',
                                    slug='category-2')]

        params = {'title': 'Product 1',
                  'content': 'Lorem ipsum',
                  'slug': 'product-1'}
        self.product = Product.objects.create(**params)
        self.product.categories.add(*self.categories)

        params = {'title': 'Product 1',
                  'content': 'Lorem ipsum',
                  'slug': 'product-1'}
        self.product2 = Product.objects.create(**params)
        self.product2.categories.add(*self.categories)

    def test_category_published_manager_get_query_set(self):
        category = Category.objects.create(
            title='Third Category', slug='third-category')
        self.assertEqual(Category.published.count(), 2)
        self.product2.categories.add(category)
        self.product2.status = PUBLISHED
        self.product2.save()
        self.assertEqual(Category.published.count(), 3)

    def test_product_published(self):
        self.product2.status = HIDDEN
        self.product2.save()
        self.assertEqual(product_published(Product.objects.all()).count(), 1)

        self.product2.status = PUBLISHED
        self.product2.save()
        self.assertEqual(product_published(Product.objects.all()).count(), 2)

        self.product.start_publication = datetime(2099, 1, 1, tzinfo=UTC)
        self.product.save()
        self.assertEqual(product_published(Product.objects.all()).count(), 1)

        self.product.start_publication = datetime(2000, 1, 1, tzinfo=UTC)
        self.product.save()
        self.assertEqual(product_published(Product.objects.all()).count(), 2)

        self.product.end_publication = datetime(2000, 1, 1, tzinfo=UTC)
        self.product.save()
        self.assertEqual(product_published(Product.objects.all()).count(), 1)

        self.product.end_publication = datetime(2099, 1, 1, tzinfo=UTC)
        self.product.save()
        self.assertEqual(product_published(Product.objects.all()).count(), 2)

    def test_entry_published_manager_get_query_set(self):

        self.product2.status = HIDDEN
        self.product2.save()
        self.assertEqual(Product.published.count(), 1)

        self.product2.status = PUBLISHED
        self.product2.save()
        self.assertEqual(Product.published.count(), 2)

        self.product.start_publication = datetime(2000, 1, 1, tzinfo=UTC)
        self.product.save()
        self.assertEqual(Product.published.count(), 2)

        self.product.end_publication = datetime(2000, 1, 1, tzinfo=UTC)
        self.product.save()
        self.assertEqual(Product.published.count(), 1)

        self.product.end_publication = datetime(2099, 1, 1, tzinfo=UTC)
        self.product.save()
        self.assertEqual(Product.published.count(), 2)


