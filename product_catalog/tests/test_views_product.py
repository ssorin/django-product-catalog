# coding=utf-8
""" Product Catalog: Product views test cases """

from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth.models import User


from product_catalog.models.category import Category
from product_catalog.models.product import Product
from django.conf import settings
from product_catalog.settings import PAGINATION

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

class ProductViewsTestCase(TestCase):
    """ """

    def setUp(self):
        params = {'title': 'Product 1',
                  'content': 'Lorem ipsum',
                  'slug': 'product-1'}

        params2 = {'title': 'Product 2',
                  'content': 'Lorem ipsum',
                  'slug': 'product-2'}

        params3 = {'title': 'Product 3',
                  'content': 'Lorem ipsum',
                  'slug': 'product-3'}

        self.product1 = Product.objects.create(**params)
        self.product2 = Product.objects.create(**params2)
        self.product3 = Product.objects.create(**params3)

    def test_product_list_view(self):
        url = reverse('product_catalog:product_list')
        response = self.client.get(url)
        self.assertEqual(PAGINATION, 10)
        self.assertTemplateUsed(response, 'product_catalog/product_list.html')
        self.assertIsNotNone(response.context['product_list'])
        self.assertEqual(response.context['product_list'][0], self.product3)
        self.assertEqual(response.context['product_list'][1], self.product2)
        self.assertEqual(response.context['product_list'][2], self.product1)

    def test_product_list_paginated(self):
        for i in range(PAGINATION):
            params = {'title': 'Paginate product %i' % i,
                      'content': 'Lorem ipsum %i' % i,
                      'slug': 'paginate-product-%i' % i
                      }
            Product.objects.create(**params)

        url = reverse('product_catalog:product_list')
        response = self.client.get(url)
        self.assertEqual(len(response.context['object_list']), PAGINATION)
        response = self.client.get(url + '?page=2')
        self.assertEqual(len(response.context['object_list']), 3)

    def test_product_detail_view(self):

        category = Category.objects.create(title='Category 1', slug='category-1')
        self.product1.categories.add(category)

        url = reverse('product_catalog:product_detail', args=[self.product1.slug])
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'product_catalog/product_detail.html')
        self.assertEqual(response.context['product'].title, self.product1.title)
        self.assertEqual(response.context['product'].content, self.product1.content)
        self.assertEqual(response.context['product'].slug, self.product1.slug)
        self.assertEqual(response.context['product'].categories, self.product1.categories)

    def create_user_and_log(self):
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password'
        )
        self.client.force_login(self.user)

    def test_product_add_view(self):
        url = reverse('product_catalog:product_add')
        response = self.client.get(url)
        # if not logged in redirect (302) to the loggin page
        self.assertEqual(response.status_code, 302)

        self.create_user_and_log()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['FRONT_MANAGEMENT'], True)
        self.assertTemplateUsed(response, 'product_catalog/product_form.html')

    def test_product_update_view(self):
        url = reverse('product_catalog:product_update', args=[self.product1.id])
        response = self.client.get(url)
        # if not logged in redirect (302) to the loggin page
        self.assertEqual(response.status_code, 302)

        self.create_user_and_log()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['FRONT_MANAGEMENT'], True)
        self.assertTemplateUsed(response, 'product_catalog/product_form.html')

    def test_product_delete_view(self):
        url = reverse('product_catalog:product_delete', args=[self.product1.id])
        response = self.client.get(url)
        # if not logged in redirect (302) to the loggin page
        self.assertEqual(response.status_code, 302)

        self.create_user_and_log()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['FRONT_MANAGEMENT'], True)
        self.assertTemplateUsed(response, 'product_catalog/product_confirm_delete.html')

