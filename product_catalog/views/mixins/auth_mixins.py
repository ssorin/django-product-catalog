# -*- coding: utf-8 -*-
""" Product Catalog: Product view mixins to control permission and authentication """

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from django.conf import settings

from product_catalog.settings import ACCESS_PERMISSION, PERMISSION_OPTIONS_SUPERUSER, \
    PERMISSION_OPTIONS_STAFF, PERMISSION_OPTIONS_OWNER

class AccessMixin(LoginRequiredMixin):
    """
    CBV mixin which verifies that the current user is authenticated
    and if he has the correct permissions (superuser / staff / owner).
    """

    required_permission = ACCESS_PERMISSION
    redirect_url = settings.LOGIN_URL

    def get_is_superuser(self):
        if self.request.user.is_superuser:
            return True
        return False

    def get_is_staff(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return True
        return False

    def get_is_owner(self):
        self.object = self.get_object()
        if self.object.owner == self.request.user or self.request.user.is_superuser:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):

        access_permission = False

        if self.required_permission == PERMISSION_OPTIONS_SUPERUSER:
            access_permission = self.get_is_superuser()

        elif self.required_permission == PERMISSION_OPTIONS_STAFF:
            access_permission = self.get_is_staff()

        elif self.required_permission == PERMISSION_OPTIONS_OWNER:
            access_permission = self.get_is_owner()

        if not access_permission:
            return redirect(settings.LOGIN_URL)

        return super(AccessMixin, self).dispatch(request, *args, **kwargs)
