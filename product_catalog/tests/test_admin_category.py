# coding=utf-8
""" Product Catalog: admin category test cases """

from __future__ import unicode_literals

from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.contrib.admin.options import ModelAdmin
from django.urls import reverse

from product_catalog.models.category import Category
from product_catalog.admin.category import CategoryAdmin

class MockRequest:
    pass

request = MockRequest()

class CategoryAdminTestCase(TestCase):
    """Test case for Product Admin"""

    def setUp(self):
        params = {'title': 'Category 1',
                  'slug': 'category-1'}
        self.category = Category.objects.create(**params)
        self.site = AdminSite()
        self.admin = CategoryAdmin(Category, admin_site=1)

    def test_modelAdmin_str(self):
        ma = ModelAdmin(Category, self.site)
        self.assertEqual(str(ma), 'product_catalog.ModelAdmin')

    def test_default_fields(self):
        ma = ModelAdmin(Category, self.site)
        self.assertEqual(list(ma.get_form(request).base_fields), ['title', 'slug', 'description', 'parent'])
        self.assertEqual(list(ma.get_fields(request)), ['title', 'slug', 'description', 'parent'])
        self.assertEqual(list(ma.get_fields(request, self.category)), ['title', 'slug', 'description', 'parent'])
        self.assertIsNone(ma.get_exclude(request, self.category))

    def test_get_view_on_site(self):
        self.assertEqual(
            self.admin.get_view_on_site(self.category),
            '<a href="/categories/category-1/" target="blank">/categories/category-1/</a>'
        )

class FunctionnalAdminTestCase(TestCase):
    """
    Functional testing admin integration.
    We just executing the view to see if the integration works.
    """

    def setUp(self):

        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password'
        )

        self.category = Category.objects.create(
            title='Category', slug='cat'
        )
        self.client.force_login(self.user)

    def assert_admin(self, url):
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_admin_product_list(self):
        self.assert_admin(
            reverse('admin:product_catalog_category_changelist')
        )

    def test_admin_product_add(self):
        self.assert_admin(
            reverse('admin:product_catalog_category_add')
        )

    def test_admin_product_update(self):
        self.assert_admin(
            reverse('admin:product_catalog_category_change', args=[self.category.pk])
        )

    def test_admin_product_delete(self):
        self.assert_admin(
            reverse('admin:product_catalog_category_delete', args=[self.category.pk])
        )
