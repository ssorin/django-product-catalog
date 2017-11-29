# coding=utf-8
""" Product Catalog: admin product test cases """

from __future__ import unicode_literals

from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.contrib.admin.options import ModelAdmin
from django.urls import reverse

from product_catalog.models.product import Product
from product_catalog.admin.product import ProductAdmin
from product_catalog.models.category import Category

class MockRequest:
    pass

request = MockRequest()


class ProductAdminTestCase(TestCase):
    """Test case for Product Admin"""

    def setUp(self):
        params = {'title': 'Product 1',
                  'content': 'Lorem ispsum',
                  'slug': 'product-1'}
        self.product = Product.objects.create(**params)
        self.site = AdminSite()
        self.admin = ProductAdmin(Product, admin_site=1)

    def test_modelAdmin_str(self):
        ma = ModelAdmin(Product, self.site)
        self.assertEqual(str(ma), 'product_catalog.ModelAdmin')

    def test_default_fields(self):
        ma = ModelAdmin(Product, self.site)
        default_list_fields = [
            'title', 'creation_date', 'categories', 'status', 'start_publication', 'end_publication',
            'excerpt', 'content', 'image', 'image_caption', 'owner'
        ]
        self.assertEqual(list(ma.get_form(request).base_fields), default_list_fields)
        self.assertEqual(list(ma.get_fields(request)), default_list_fields)
        self.assertEqual(list(ma.get_fields(request, self.product)), default_list_fields)
        self.assertIsNone(ma.get_exclude(request, self.product))

    # todo: test_save_related(self):
    # def test_save_related(self):
    #     pass

    def test_get_categories(self):
        category_1 = Category.objects.create(title='Category <b>1</b>',
                                             slug='category-1')
        category_2 = Category.objects.create(title='Category <b>2</b>',
                                             slug='category-2')
        self.product.categories.add(category_1)
        self.product.categories.add(category_2)

        self.assertEqual(
            self.admin.get_categories(self.product),
            '<a href="/categories/category-1/" target="blank">Category &lt;b&gt;1&lt;/b&gt;</a>, '
            '<a href="/categories/category-2/" target="blank">Category &lt;b&gt;2&lt;/b&gt;</a>'
        )

    def test_get_categories_non_ascii(self):
        category = Category.objects.create(title='Catégory тест', slug='category-slug')
        self.product.categories.add(category)
        self.assertEqual(
            self.admin.get_categories(self.product),
            '<a href="/categories/category-slug/" target="blank">Catégory тест</a>'
        )

    def test_get_is_visible(self):
        self.assertEqual(self.admin.get_is_visible(self.product),
                         self.product.is_visible)

    def test_get_thumbnail(self):
        self.assertIsNone(self.admin.get_thumbnail(self.product))
        self.product.image = '/image/test.jpg'
        self.product.save()
        self.assertEqual(
            self.admin.get_thumbnail(self.product),
            '<a href="/media/image/test.jpg" target="_blank"><img src="/media/image/test.jpg" width=80/></a>'
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
        params = {
            'title': 'My title',
            'content': 'My content',
            'slug': 'my-title'
        }
        self.product = Product.objects.create(**params)
        self.client.force_login(self.user)

    def assert_admin(self, url):
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_admin_product_list(self):
        self.assert_admin(
            reverse('admin:product_catalog_product_changelist')
        )

    def test_admin_product_add(self):
        self.assert_admin(
            reverse('admin:product_catalog_product_add')
        )

    def test_admin_product_update(self):
        self.assert_admin(
            reverse('admin:product_catalog_product_change', args=[self.product.pk])
        )

    def test_admin_product_delete(self):
        self.assert_admin(
            reverse('admin:product_catalog_product_delete', args=[self.product.pk])
        )
