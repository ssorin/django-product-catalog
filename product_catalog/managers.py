"""Managers of Zinnia"""

from django.db import models
from django.utils import timezone

DRAFT = 0
HIDDEN = 1
PUBLISHED = 2

def entries_published(queryset):
    """
    Return only the entries published.
    """
    now = timezone.now()
    return queryset.filter(
        models.Q(start_publication__lte=now) |
        models.Q(start_publication=None),
        models.Q(end_publication__gt=now) |
        models.Q(end_publication=None),
        status=PUBLISHED)


class EntryPublishedManager(models.Manager):
    """
    Manager to retrieve published entries.
    """

    def get_queryset(self):
        """
        Return published entries.
        """
        return entries_published(
            super(EntryPublishedManager, self).get_queryset())
