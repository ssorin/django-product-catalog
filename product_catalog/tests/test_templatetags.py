# coding=utf-8
""" Product Catalog: templateTags test cases """


from django.test import TestCase
from django.template import Context

from product_catalog.models.product import Product
from product_catalog.models.category import Category
from product_catalog.templatetags.product_catalog import get_categories
from product_catalog.templatetags.product_catalog import get_last_products
from product_catalog.managers import PUBLISHED, DRAFT, HIDDEN

class TemplateTagsTestCase(TestCase):
    """Test cases for Template tags"""

    def setUp(self):
        params = {'title': 'Product 1',
                  'content': 'Lorem ipsum',
                  'slug': 'product-1'}
        self.product = Product.objects.create(**params)

    def test_get_categories(self):
        source_context = Context()

        with self.assertNumQueries(0):
            context = get_categories(source_context)

        self.assertEqual(len(context['categories']), 0)
        self.assertEqual(context['template'], 'product_catalog/tags/categories.html')
        self.assertEqual(context['context_category'], None)
        category = Category.objects.create(title='Category 1',
                                           slug='category-1')
        self.product.categories.add(category)

        source_context = Context({'category': category})
        with self.assertNumQueries(0):
            context = get_categories(source_context, 'custom_template.html')
        self.assertEqual(len(context['categories']), 1)
        self.assertEqual(context['template'], 'custom_template.html')
        self.assertEqual(context['context_category'], category)


    def test_get_last_products(self):
        source_context = Context()

        with self.assertNumQueries(0):
            context = get_last_products()
        self.assertEqual(context['template'], 'product_catalog/tags/last_products.html')

        with self.assertNumQueries(0):
            context = get_last_products(template='custom_template.html')
        self.assertEqual(context['template'], 'custom_template.html')

        self.product.status = HIDDEN
        self.product.save()
        with self.assertNumQueries(0):
            context = get_last_products()
        self.assertEqual(len(context['products']), 0)

        self.product.status = PUBLISHED
        self.product.save()
        with self.assertNumQueries(0):
            context = get_last_products()
        self.assertEqual(len(context['products']), 1)

        params = {'title': 'Product 2',
                  'content': 'Lorem ipsum',
                  'slug': 'product-2'}
        Product.objects.create(**params)
        with self.assertNumQueries(0):
            context = get_last_products(3)
        self.assertEqual(len(context['products']), 2)

        with self.assertNumQueries(0):
            context = get_last_products(1)
        self.assertEqual(len(context['products']), 1)

