# -*- coding: utf-8 -*-
""" Product Catalog: Product models"""

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from product_catalog.settings import UPLOAD_TO
from product_catalog.managers import DRAFT, HIDDEN, PUBLISHED
from product_catalog.managers import ProductPublishedManager
from product_catalog.models.category import Category

from django_extensions.db.fields import AutoSlugField

@python_2_unicode_compatible
class BaseProduct(models.Model):
    """
    Abstract base product model class providing the base fields and methods
    """
    title = models.CharField(_('title'), max_length=255)
    slug = AutoSlugField(_('slug'), max_length=255, populate_from=['title', 'id'], unique=True, db_index=True)
    creation_date = models.DateTimeField(_('creation date'), default=timezone.now)
    last_update = models.DateTimeField(_('last update'), auto_now=True)
    categories = models.ManyToManyField(Category,
                                        blank=True,
                                        related_name='products',
                                        verbose_name=_('categories'))
    objects = models.Manager()

    @models.permalink
    def get_absolute_url(self):
        """ """
        return 'product_catalog:product_detail', (self.slug,)

    def __str__(self):
        return '%s' % self.title

    class Meta:
        """
        BaseProduct's meta informations.
        """
        abstract = True
        ordering = ['-creation_date']
        get_latest_by = 'creation_date'
        verbose_name = _('product')
        verbose_name_plural = _('products')



class PublicationProduct(models.Model):
    """
    Abstract model class providing the publication fields and methods
    """

    STATUS_CHOICES = ((DRAFT, _('draft')),
                      (HIDDEN, _('hidden')),
                      (PUBLISHED, _('published')))

    status = models.IntegerField(_('status'), db_index=True, choices=STATUS_CHOICES, default=PUBLISHED)
    start_publication = models.DateTimeField(_('start publication'), blank=True, null=True,
                                             help_text=_('Start date of publication.'))
    end_publication = models.DateTimeField(_('end publication'), blank=True, null=True,
                                           help_text=_('End date of publication.'))

    published = ProductPublishedManager()

    class Meta:
        abstract = True

    @property
    def is_actual(self):
        """
        Checks if a product is in its publication period.
        """
        now = timezone.now()
        if self.start_publication and now < self.start_publication:
            return False

        if self.end_publication and now >= self.end_publication:
            return False
        return True

    @property
    def is_visible(self):
        """
        Checks if a product is visible and published.
        """
        return self.is_actual and self.status == PUBLISHED

    @property
    def previous_entry(self):
        """
        Returns the previous published entry if exists.
        """
        return self.previous_next_entries[0]

    @property
    def next_entry(self):
        """
        Returns the next published entry if exists.
        """
        return self.previous_next_entries[1]

    @property
    def previous_next_entries(self):
        """
        Returns and caches a tuple containing the next
        and previous published entries.
        Only available if the entry instance is published.
        """
        previous_next = getattr(self, 'previous_next', None)

        if previous_next is None:
            if not self.is_visible:
                previous_next = (None, None)
                setattr(self, 'previous_next', previous_next)
                return previous_next

            entries = list(self.__class__.published.all())
            index = entries.index(self)
            try:
                previous = entries[index + 1]
            except IndexError:
                previous = None

            if index:
                _next = entries[index - 1]
            else:
                _next = None
            previous_next = (previous, _next)
            setattr(self, 'previous_next', previous_next)
        return previous_next



class ExcerptProduct(models.Model):
    """
    Abstract model class providing field
    and methods to write excerpt for a product.
    """
    excerpt = models.TextField(_('excerpt'), blank=True, max_length=70,
                               help_text=_('Max length: 70 characters'))

    class Meta:
        abstract = True

class ContentProduct(models.Model):
    """
    Abstract content model class providing field
    and methods to write product content.
    """
    content = models.TextField(_('content'), blank=True)

    class Meta:
        abstract = True


class ImageProduct(models.Model):
    """
    Abstract model class to add an image.
    """

    image = models.ImageField(_('image'), blank=True, upload_to=UPLOAD_TO)
    image_caption = models.CharField(_('caption'), blank=True, help_text=_("Image's caption."), max_length=250)

    class Meta:
        abstract = True

class OwnerProduct(models.Model):
    """ Abstract class to add an owner to the the product """
    owner = models.ForeignKey(User, blank=True, null=True, related_name='products', verbose_name=_('owner'))

    class Meta:
        abstract = True


class AbstractProduct(
        BaseProduct,
        PublicationProduct,
        ImageProduct,
        ExcerptProduct,
        ContentProduct,
        OwnerProduct,
):
    """
    Final abstract product model class assembling
    all the abstract product model classes into a single one.
    In this manner we can override some fields without
    reimplementing all the AbstractProduct.
    """

    class Meta(BaseProduct.Meta):
        abstract = True
