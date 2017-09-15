""" Product Catalog: Product models"""

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class CoreEntry(models.Model):
    """
    Abstract core entry model class providing
    the fields and methods required for publishing
    content over time.
    """
    # STATUS_CHOICES = ((DRAFT, _('draft')),
    #                   (HIDDEN, _('hidden')),
    #                   (PUBLISHED, _('published')))

    title = models.CharField(
        _('title'), max_length=255)

    slug = models.SlugField(
        _('slug'), max_length=255,
        unique_for_date='publication_date',
        help_text=_("Used to build the entry's URL."))

    # status = models.IntegerField(
    #     _('status'), db_index=True,
    #     choices=STATUS_CHOICES, default=DRAFT)

    publication_date = models.DateTimeField(
        _('publication date'),
        db_index=True, default=timezone.now,
        help_text=_("Used to build the entry's URL."))

    start_publication = models.DateTimeField(
        _('start publication'),
        db_index=True, blank=True, null=True,
        help_text=_('Start date of publication.'))

    end_publication = models.DateTimeField(
        _('end publication'),
        db_index=True, blank=True, null=True,
        help_text=_('End date of publication.'))

    creation_date = models.DateTimeField(
        _('creation date'),
        default=timezone.now)

    last_update = models.DateTimeField(
        _('last update'), default=timezone.now)

    objects = models.Manager()
    # published = EntryPublishedManager()

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

    # @property
    # def is_visible(self):
    #     """
    #     Checks if an entry is visible and published.
    #     """
    #     return self.is_actual and self.status == PUBLISHED

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

    def save(self, *args, **kwargs):
        """
        Overrides the save method to update the
        the last_update field.
        """
        self.last_update = timezone.now()
        super(CoreEntry, self).save(*args, **kwargs)

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
        ordering = ['-publication_date']
        get_latest_by = 'publication_date'
        verbose_name = _('product')
        verbose_name_plural = _('products')
        # index_together = [['slug', 'publication_date'],
        #                   ['status', 'publication_date',
        #                    'start_publication', 'end_publication']]
        # permissions = (('can_view_all', 'Can view all entries'),
        #                ('can_change_status', 'Can change status'),
        #                ('can_change_author', 'Can change author(s)'), )


class ContentEntry(models.Model):
    """
    Abstract content model class providing field
    and methods to write content inside an entry.
    """
    content = models.TextField(_('content'), blank=True)



    class Meta:
        abstract = True





class CategoriesEntry(models.Model):
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




class AbstractEntry(
        CoreEntry,
        ContentEntry,
        CategoriesEntry,
):
    """
    Final abstract entry model class assembling
    all the abstract entry model classes into a single one.
    In this manner we can override some fields without
    reimplemting all the AbstractEntry.
    """

    class Meta(CoreEntry.Meta):
        abstract = True


class Product(AbstractEntry):
    pass
