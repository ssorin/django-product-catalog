# coding=utf-8
""" Product Catalog: models product test cases """

from pytz import UTC
from datetime import datetime

from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User

from product_catalog.models.product import Product
from product_catalog.models.category import Category
from product_catalog.managers import PUBLISHED, DRAFT, HIDDEN


class EntryTestCase(TestCase):

    def setUp(self):
        params = {'title': 'Product 1',
                  'content': 'Lorem ipsum',
                  'slug': 'product-1'}
        self.product = Product.objects.create(**params)

    def test_create_product(self):

        params_category = {'title': 'Category 1', 'slug': 'category-1'}
        category_1 = Category.objects.create(**params_category)

        params_user = {'username': 'admin', 'email': 'admin@example.com', 'password': 'password'}
        user = User.objects.create_superuser(**params_user)

        params = {
                    'title':             'Product test',
                    'slug':              'product-test',
                    'start_publication': datetime(2099, 11, 28, tzinfo=UTC),
                    'end_publication':   datetime(2099, 11, 28, tzinfo=UTC),
                    'content':           'Lorem ipsum content',
                    'excerpt':           'Lorem ipsum excerpt',
                    'image':             '/image/image-product-test.jpg',
                    'image_caption':     'Lorem ipsum image caption',
                    'owner':             user
                  }

        product = Product.objects.create(**params)
        product.categories.add(category_1)

        self.assertEqual(product.title, 'Product test')
        self.assertEqual(product.slug, 'product-test')
        self.assertEqual(product.start_publication, datetime(2099, 11, 28, tzinfo=UTC))
        self.assertEqual(product.end_publication, datetime(2099, 11, 28, tzinfo=UTC))
        self.assertEqual(product.content, 'Lorem ipsum content')
        self.assertEqual(product.excerpt, 'Lorem ipsum excerpt')
        self.assertEqual(product.image, '/image/image-product-test.jpg')
        self.assertEqual(product.image_caption,'Lorem ipsum image caption')
        self.assertEqual(product.owner, user)
        self.assertEqual(product.categories.get(pk=category_1.pk), category_1)
        self.assertTrue(product.creation_date)
        self.assertTrue(product.last_update)

    def test_get_absolute_url(self):
        self.assertEqual('/products/product-1/', self.product.get_absolute_url())

    def test_str(self):
        self.assertEqual(str(self.product), 'Product 1')

    def test_is_actual(self):
        self.assertTrue(self.product.is_actual)
        self.product.start_publication = datetime(2099, 11, 28, tzinfo=UTC)
        self.assertFalse(self.product.is_actual)
        self.product.start_publication = timezone.now()
        self.assertTrue(self.product.is_actual)
        self.product.end_publication = datetime(2015, 11, 28, tzinfo=UTC)
        self.assertFalse(self.product.is_actual)

    def test_is_visible(self):
        self.assertTrue(self.product.is_visible)

        self.product.status = DRAFT
        self.assertFalse(self.product.is_visible)

        self.product.status = HIDDEN
        self.assertFalse(self.product.is_visible)

        self.product.status = PUBLISHED
        self.assertTrue(self.product.is_visible)

        self.product.start_publication = datetime(2099, 11, 28, tzinfo=UTC)
        self.assertFalse(self.product.is_visible)

        self.product.start_publication = timezone.now()
        self.assertTrue(self.product.is_actual)

        self.product.end_publication = datetime(2015, 11, 28, tzinfo=UTC)
        self.assertFalse(self.product.is_actual)

    def test_previous_entry(self):
        self.product.status = PUBLISHED
        self.product.save()
        self.assertFalse(self.product.previous_entry)

        params = {'title': 'Product 2',
                  'content': 'Lorem ispum',
                  'slug': 'product-2',
                  'status': PUBLISHED}
        self.product2 = Product.objects.create(**params)
        self.assertTrue(self.product2.previous_entry)
        self.assertEqual(self.product2.previous_entry, self.product)
        self.assertIsNone(self.product.previous_entry)

        params = {'title': 'Product 3',
                  'content': 'Lorem ispum',
                  'slug': 'product-3',
                  'status': PUBLISHED}
        self.product3 = Product.objects.create(**params)
        self.assertTrue(self.product3.previous_entry)
        self.assertEqual(self.product3.previous_entry, self.product2)
        self.assertIsNone(self.product.previous_entry)

    def test_next_entry(self):

        self.product.status = PUBLISHED
        self.product.save()
        self.assertFalse(self.product.next_entry)
        del self.product.previous_next

        params = {'title': 'Product 2',
                  'content': 'Lorem ispum',
                  'slug': 'product-2',
                  'status': PUBLISHED}
        self.product2 = Product.objects.create(**params)
        self.assertFalse(self.product2.next_entry)
        self.assertEqual(self.product.next_entry, self.product2)

        params = {'title': 'Product 3',
                  'content': 'Lorem ispum',
                  'slug': 'product-3',
                  'status': PUBLISHED}
        self.product3 = Product.objects.create(**params)
        del self.product2.previous_next
        self.assertFalse(self.product3.next_entry)
        self.assertEqual(self.product2.next_entry, self.product3)
