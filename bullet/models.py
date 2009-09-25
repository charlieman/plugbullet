from django.db import models
from datetime import datetime
from calendar import monthrange

# Create your models here.


class EventManager(models.Manager):

    def month_events(self, year=None, month=None, so_far=False):
        """Retrieves events for given month"""
        _now = datetime.now()

        year = year or _now.year
        month = month or _now.month

        month_start = datetime(year, month, day=1)

        month_end = _now if so_far else datetime(year, month,
                                            day=monthrange(year, month)[1])

        return self.filter(active=True,
                           start_date__gte=month_start,
                           end_date__lte=month_end).order_by('start_date')

    def prob_random(self, limit=1, exclude=None):
        """Retrieves random events with probability based on
        date closeness (weight)"""

        result = self.month_events()
        if exclude:
            result = result.exclude(id=exclude.id)

        month_start = datetime.now().replace(day=1)

        for event in result:
            weight = (event.start_date - month_start).days


class Type(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=128)
    url = models.URLField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    comment = models.CharField(max_length=128)

    # 3 letter codes for locations
    # Check django.contrib.localflavor.pe.pe_region
    region = models.CharField(max_length=3)

    address = models.CharField(max_length=128)


    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    active = models.BooleanField(default=False)

    # For now each event is of one type, maybe a ManyToMany should be used
    type = models.ForeignKey(Type)

    # This could become their own model....
    organization = models.CharField(max_length=128)
    organization_url = models.URLField()

    # So could this...
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name
