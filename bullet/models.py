from django.db import models
from datetime import datetime
from calendar import monthrange
from random import randint

# Create your models here.


class BulletManager(models.Manager):

    def month_events(self, year=None, month=None, from_now=None):
        """Retrieves events for given month
        set from_now=True for retrieving this months events from now
        until the end of the month"""
        _now = datetime.now()

        year = year or _now.year
        month = month or _now.month

        month_start = _now if from_now else datetime(year, month, day=1)

        month_end = datetime(year, month, day=monthrange(year, month)[1])

        return self.filter(active=True,
                           start_date__gte=month_start,
                           end_date__lte=month_end).order_by('start_date')

    def comming_soon(self, exclude=None):
        """Retrieves a random event with probability based on
        date closeness (weight)"""
        # TODO: return several events based on a limit parameter
        result = self.month_events(from_now=True)

        if exclude:
            result = result.exclude(id=exclude.id)

        _now = datetime.now()

        weight = [( 31 - (event.start_date if event.start_date > _now else event.end_date) - _now).days for event in result]
        _min = min(weight)
        _sum = sum(weight)

        # maybe should use izip for optimization?
        # from itertools import izip
        _data = zip(weight, result)
        _data.sort()

        overweight = 0
        n = randint(_min, _sum)

        for w, e in _data:
            overweight += w
            if overweight >= n - 1:
                return e
                break # is this necessary?

        # it should never get here
        return result


class Type(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name


class Bullet(models.Model):
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

    objects = BulletManager()

    def __unicode__(self):
        return self.name

