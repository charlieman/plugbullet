from django.db import models
from datetime import datetime
from random import randint

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

import constants


class BulletManager(models.Manager):

    def month_events(self, year=None, month=None, from_now=None):
        """Retrieves events for given month
        set from_now=True for retrieving this months events from now
        until the end of the month"""
        _now = datetime.now()

        year = year or _now.year
        month = month or _now.month

        first_day = _now if from_now else _now.replace(day=1)

        if first_day.month == 12:
            last_day = first_day.replace(year=first_day.year + 1, month=1)
        else:
            last_day = first_day.replace(month=first_day.month + 1)

        return self.filter(active=True,
                           start_date__gte=first_day,
                           end_date__lt=last_day).order_by('start_date')

    def comming_soon(self, exclude=None):
        """Retrieves a random event with probability based on
        date closeness (weight)"""
        # TODO: return several events based on a limit parameter

        # only show events since this moment
        result = self.month_events(from_now=True)

        if exclude:
            result = result.exclude(id=exclude.id)

        _now = datetime.now()

        # This will give you a number -a weight- based on the distance
        # of the day from now.
        # if today is 10 and it starts 15 then weight = 31 - (15 - 10) = 26
        # if today is 15 and it started 13 and ends 17 then
        # weight = 31 - (17 - 15) = 29
        # if today is 2 and it starts 20 then weight = 31 - (20 - 2) = 13
        # TODO: give even more weight to events happening right now, in the next 2 days and next 7 days
        weight = [(31 - (event.start_date if event.start_date > _now else event.end_date) - _now).days for event in result]
        _min = min(weight)
        _sum = sum(weight)

        # maybe should use izip for optimization?
        # from itertools import izip
        _data = zip(weight, result)
        _data.sort()

        overweight = 0
        n = randint(_min, _sum)

        for _weight, _event in _data:
            overweight += _weight
            if overweight >= n - 1:
                return _event

        # it should never get here
        return result


class Type(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=128)

    class Meta:
        verbose_name = _('type')
        verbose_name_plural = _('types')

    def __unicode__(self):
        return self.name


class Address(models.Model):
    # 3 letter codes for locations
    # Check django.contrib.localflavor.pe.pe_region
    region = models.CharField(max_length=3)
    address = models.CharField(max_length=128)
    # the place can have a name? ej "Auditorio xxx"
    name = models.CharField(max_length=128, blank=True)

    def __unicode__(self):
        return self.address


class Organization(models.Model):
    name = models.CharField(max_length=128)
    url = models.URLField()

    def __unicode__(self):
        return self.name


class Bullet(models.Model):
    name = models.CharField(max_length = 128)
    url = models.URLField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    comment = models.CharField(max_length = 128)

    created_at = models.DateTimeField(auto_now_add = True)
    edited_at = models.DateTimeField(auto_now = True)

    status = models.PositiveIntegerField(choices = constants.STATUS_CHOICES)

    # For now each event is of one type, maybe a ManyToMany should be used
    type = models.ForeignKey(Type)
    address = models.ForeignKey(Address)
    organization = models.ForeignKey(Organization)
    contact = models.ForeignKey(User, related_name="contact", editable=False)
    objects = BulletManager()

    def __unicode__(self):
        return self.name
