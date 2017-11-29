# coding=utf-8
""" Product Catalog: context processors test cases """


from product_catalog.settings import FRONT_MANAGEMENT
from django.test import TestCase, override_settings

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

class ContextProcessorTestCase(TestCase):
    """Test case for Product Admin"""

    def test_product_front_management(self):
        response = self.client.get('/')
        self.assertEqual(response.context['FRONT_MANAGEMENT'], FRONT_MANAGEMENT)
