# coding=utf-8
""" Product Catalog: models product test cases """


from django.test import TestCase

from product_catalog import settings

class SettingsTestCase(TestCase):

    def test_settings(self):

        self.assertIsNotNone(settings.PAGINATION)
        self.assertIsNotNone(settings.PRODUCT_BASE_MODEL)
        self.assertIsNotNone(settings.UPLOAD_TO)
        self.assertIsNotNone(settings.FRONT_MANAGEMENT)
        self.assertIsNotNone(settings.PERMISSION_OPTIONS_SUPERUSER)
        self.assertIsNotNone(settings.PERMISSION_OPTIONS_STAFF)
        self.assertIsNotNone(settings.PERMISSION_OPTIONS_OWNER)
        self.assertIsNotNone(settings.ACCESS_PERMISSION)
        self.assertIsNotNone(settings.FORM_FIELDS)
        self.assertIsNotNone(settings.FORM_UPDATE_FIELDS)
        self.assertIsNotNone(settings.FORM_CREATE_FIELDS)
