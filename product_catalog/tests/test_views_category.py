# coding=utf-8
""" Product Catalog: category views test cases """

from django.test import TestCase, override_settings
from django.urls import reverse

from product_catalog.models.category import Category
from product_catalog.models.product import Product

@override_settings(
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                    'product_catalog.context_processors.product_front_management'
                ],
            },
        },
    ]
)

class CategoryViewsTestCase(TestCase):
    """ """

    def setUp(self):
        self.category = Category.objects.create(title='Category 1', slug='category-1')
        self.category2 = Category.objects.create(title='Category 2', slug='category-2')
        self.category3 = Category.objects.create(title='Category 3', slug='category-3')

    def test_category_list_view(self):
        url = reverse('product_catalog:category_list')
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'product_catalog/category_list.html')
        self.assertIsNotNone(response.context['category_list'])
        self.assertEqual(response.context['category_list'][0], self.category)
        self.assertEqual(response.context['category_list'][1], self.category2)
        self.assertEqual(response.context['category_list'][2], self.category3)

    def test_category_detail_view(self):
        url = reverse('product_catalog:category_detail', args=[self.category.slug])
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'product_catalog/category_detail.html')
        self.assertEqual(response.context['category'], self.category)
        self.assertEqual(len(response.context['product_list']), 0)

        params = {'title': 'Product 1',
                  'content': 'Lorem ipsum',
                  'slug': 'product-1'}
        params2 = {'title': 'Product 2',
                  'content': 'Lorem ipsum',
                  'slug': 'product-2'}
        params3 = {'title': 'Product 3',
                  'content': 'Lorem ipsum',
                  'slug': 'product-3'}

        product1 = Product.objects.create(**params)
        product2 = Product.objects.create(**params2)
        product3 = Product.objects.create(**params3)

        product1.categories.add(self.category2)
        product2.categories.add(self.category)
        product3.categories.add(self.category)

        url = reverse('product_catalog:category_detail', args=[self.category.slug])
        response = self.client.get(url)
        self.assertEqual(len(response.context['product_list']), 2)
        self.assertEqual(response.context['product_list'][0], product3)
        self.assertEqual(response.context['product_list'][1], product2)

        url = reverse('product_catalog:category_detail', args=[self.category2.slug])
        response = self.client.get(url)
        self.assertEqual(len(response.context['product_list']), 1)
        self.assertEqual(response.context['product_list'][0], product1)

        product1.categories.add(self.category)
        url = reverse('product_catalog:category_detail', args=[self.category.slug])
        response = self.client.get(url)
        self.assertEqual(len(response.context['product_list']), 3)
        self.assertEqual(response.context['product_list'][0], product3)
        self.assertEqual(response.context['product_list'][1], product2)
        self.assertEqual(response.context['product_list'][2], product1)