# coding=utf-8
""" Product Catalog: urls test cases """

from django.test import TestCase
from django.urls import reverse
from django.urls import resolve

from product_catalog.models.product import Product
from product_catalog.models.category import Category


class UrlsTestCase(TestCase):

    def setUp(self):
        params = {'title': 'Product 1',
                  'content': 'Lorem ipsum',
                  'slug': 'product-1'}
        self.product = Product.objects.create(**params)

        self.category = Category.objects.create(title='Category 1',
                                                slug='category-1')

    def test_category_urls(self):
        url = reverse('product_catalog:category_list')
        self.assertEqual(url, '/categories/')

        url = reverse('product_catalog:category_detail', args=[self.category.slug])
        self.assertEqual(url, '/categories/%s/' % self.category.slug)

    def test_product_urls(self):
        url = reverse('product_catalog:product_list')
        self.assertEqual(url, '/products/')

        url = reverse('product_catalog:product_detail', args=[self.product.slug])
        self.assertEqual(url, '/products/%s/' % self.product.slug)

        url = reverse('product_catalog:product_home')
        self.assertEqual(url, '/')

        url = reverse('product_catalog:product_add')
        self.assertEqual(url, '/products/add/')

        url = reverse('product_catalog:product_update', args=[self.product.id])
        self.assertEqual(url, '/products/update/%s/' % self.product.pk)

        url = reverse('product_catalog:product_delete', args=[self.product.id])
        self.assertEqual(url, '/products/delete/%s/' % self.product.pk)
