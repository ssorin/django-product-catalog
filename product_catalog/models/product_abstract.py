""" Product Catalog: Product models"""

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from product_catalog.settings import UPLOAD_TO
from product_catalog.managers import DRAFT, HIDDEN, PUBLISHED
from product_catalog.managers import EntryPublishedManager


@python_2_unicode_compatible
class CoreProduct(models.Model):
    """
    Abstract core product model class providing the base fields and methods
    """
    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'), max_length=255)
    creation_date = models.DateTimeField(_('creation date'), default=timezone.now)
    last_update = models.DateTimeField(_('last update'), auto_now=True)

    objects = models.Manager()

    @models.permalink
    def get_absolute_url(self):
        """
        Builds and returns the category's URL
        based on his tree path.
        """
        return 'product_catalog:product_detail', (self.slug,)

    def __str__(self):
        return '%s' % self.title

    class Meta:
        """
        CoreEntry's meta informations.
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

    status = models.IntegerField(_('status'), db_index=True, choices=STATUS_CHOICES, default=DRAFT)
    start_publication = models.DateTimeField(_('start publication'), db_index=True, blank=True, null=True,
                                             help_text=_('Start date of publication.'))
    end_publication = models.DateTimeField(_('end publication'), db_index=True, blank=True, null=True,
                                           help_text=_('End date of publication.'))

    published = EntryPublishedManager()

    @property
    def is_actual(self):
        """
        Checks if an entry is within his publication period.
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
        Checks if an entry is visible and published.
        """
        return self.is_actual and self.status == PUBLISHED

class ExcerptProduct(models.Model):
    """
    Abstract model class providing field
    and methods to write excerpt inside an entry.
    """
    excerpt = models.TextField(_('excerpt'), blank=True, max_length=70)

    class Meta:
        abstract = True

class ContentProduct(models.Model):
    """
    Abstract content model class providing field
    and methods to write content inside an entry.
    """
    content = models.TextField(_('content'), blank=True)

    class Meta:
        abstract = True


class CategoriesProduct(models.Model):
    """
    Abstract model class to categorize the entries.
    """
    categories = models.ManyToManyField(
        'product_catalog.Category',
        blank=True,
        related_name='entries',
        verbose_name=_('categories'))

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



class AbstractProduct(
        CoreProduct,
        PublicationProduct,
        ImageProduct,
        ExcerptProduct,
        ContentProduct,
        CategoriesProduct,
):
    """
    Final abstract entry model class assembling
    all the abstract entry model classes into a single one.
    In this manner we can override some fields without
    reimplemting all the AbstractEntry.
    """

    class Meta(CoreProduct.Meta):
        abstract = True

