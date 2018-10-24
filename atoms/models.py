import logging

from django.db import models
from polymorphic.models import PolymorphicModel

logger = logging.getLogger(__name__)


class UIDMixin:
    @property
    def uid(self):
        return '{}__{}'.format(self.__class__.__name__, self.id)


class Source(models.Model, UIDMixin):
    title = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.title


class Item(PolymorphicModel, UIDMixin):
    source = models.ForeignKey(Source, on_delete=models.CASCADE)

    title = models.CharField(max_length=512)
    items = models.ManyToManyField('self', blank=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        if self.title:
            return self.title

        return self.uid

    def get_text(self):
        return self.title


class Text(Item):
    content = models.TextField()

    def get_text(self):
        text = super().get_text()
        return '{} {}'.format(text, self.content)


class Media(Item):
    url = models.URLField(max_length=512)
    credit = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Media'


class Location(Item):
    lat = models.FloatField()
    lon = models.FloatField()
    zoom = models.PositiveSmallIntegerField(blank=True, null=True)
