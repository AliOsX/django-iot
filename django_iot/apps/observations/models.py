from django.db import models
from django.core.urlresolvers import reverse


class BaseAttribute(models.Model):
    # created
    created_at = models.DateTimeField(auto_now_add=True)

    # time that the attribute is valid
    # may be different than the time it was created
    # adding the index is important because it's used for sorting
    valid_at = models.DateTimeField(db_index=True)

    # device that's the source of the attribute
    device = models.ForeignKey('devices.Device')

    class Meta:
        abstract = True
        get_latest_by = 'valid_at'


class Attribute(BaseAttribute):
    # numerical value of the attribute
    value = models.FloatField()

    # units of the numerical value
    # you may want to add choices to this
    # adding the index is important because it's used for filtering
    units = models.CharField(max_length=10, db_index=True)

    def get_absolute_url(self):
        return reverse('attribute-detail', kwargs={'pk': self.pk})


class PowerStatus(BaseAttribute):
    # true if on, false if off
    is_on = models.BooleanField()

    def get_absolute_url(self):
        return reverse('powerstatus-detail', kwargs={'pk': self.pk})


class Color(BaseAttribute):
    # hex color
    hex_string = models.CharField(max_length=7)

    def get_absolute_url(self):
        return reverse('color-detail', kwargs={'pk': self.pk})
