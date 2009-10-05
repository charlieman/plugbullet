from django.db import models
from datetime import datetime
from random import randint

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models import Q

import bullet.constants as constants


class Address(models.Model):
    # 3 letter codes for locations
    # Check django.contrib.localflavor.pe.pe_region
    region = models.CharField(max_length=3)
    address = models.CharField(max_length=128)
    # the place can have a name? ej "Auditorio xxx"
    name = models.CharField(max_length=128, blank=True)

    class Meta:
        verbose_name = _('address')
        verbose_name_plural = _('address')

    def __unicode__(self):
        return self.address


class Organization(models.Model):
    name = models.CharField(max_length=128)
    url = models.URLField()

    class Meta:
        verbose_name = _('organization')
        verbose_name_plural = _('organizations')

    def __unicode__(self):
        return self.name

class EmailChannel(models.Model):
    sender_email = models.EmailField(max_length = 128)
    sender_name = models.CharField(max_length = 128)
    mailing_list_email = models.EmailField(max_length = 128)

    class Meta:
        verbose_name = _('email channel')
        verbose_name_plural = _('email channels')

    def __unicode__(self):
        return self.name

class TwitterChannel(models.Model):
    access_token_key = models.CharField(max_length=256, blank=True)
    access_token_secret = models.CharField(max_length=256, blank=True)

    class Meta:
        verbose_name = _('twitter channel')
        verbose_name_plural = _('twitter channels')

    def __unicode__(self):
        return self.name

class Bulletin(models.Model):
    name = models.CharField(max_length = 128)
    slug = models.SlugField(max_length = 128)
    description = models.TextField()
    email_channels = models.ManyToManyField(EmailChannel, null=True)
    email_enabled = models.BooleanField(defaults=True)
    twitter_channels = models.ManyToManyField(TwitterChannel, null=True)
    twitter_enabled = models.BooleanField(defaults=True)
    created_by = models.ForeignKey(User, related_name="submissions", editable=False)
    organization = models.ForeignKey(Organization)
    created_at = models.DateTimeField(auto_now_add = True)
    edited_at = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name = _('bulletin')
        verbose_name_plural = _('bulletins')

    def __unicode__(self):
        return self.name

class BulletinEdition(models.Model):
    name = models.CharField(max_length = 128)
    slug = models.SlugField(max_length = 128)
    description = models.TextField()
    bulletin = models.ForeignKey(Bulletin, related_name='editions')
    delivery_ts = models.DateTime(blank=True, null=True)
    delivered = models.BooleanField(default=False)
    period_start = models.DateTime()
    period_end = models.DateTime()
    submission_period_start = models.DateTime()
    submission_period_end = models.DateTime()
    created_by = models.ForeignKey(User, related_name="submissions", editable=False)
    organization = models.ForeignKey(Organization)
    created_at = models.DateTimeField(auto_now_add = True)
    edited_at = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name = _('bulletin')
        verbose_name_plural = _('bulletins')

    def __unicode__(self):
        return self.name

class Submission(models.Model):
    title = models.CharField(max_length = 128)
    body = models.TextField()
    url = models.URLField()
    submitted_by = models.ForeignKey(User, related_name="submissions", editable=False)
    organization = models.ForeignKey(Organization)
    status = models.PositiveIntegerField(choices=constants.SUBMISSION_STATUS_CHOICES)
    editions = models.ManyToManyField(BulletinEdition)
    created_at = models.DateTimeField(auto_now_add = True)
    edited_at = models.DateTimeField(auto_now = True)

    # Custom manager
    objects = SubmissionManager()

    class Meta:
        verbose_name = _('Submission')
        verbose_name_plural = _('Submissions')
        abstract = True

    def __unicode__(self):
        return self.name

class EventManager(models.Manager):

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

        return self.filter(Q(start_ts__gte=first_day) | \
                Q(end_ts__lt=last_day), active=True).order_by('start_date')

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
        # TODO: give even more weight to events happening right now,
        #       in the next 2 days and next 7 days
        weight = [(31 - (ev.start_date \
                  if ev.start_date > _now else ev.end_date) - _now).days \
                  for ev in result]
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

class Event(Submission):

    start_ts = models.DatetimeField()
    end_ts = models.DatetimeField()
    paid = models.BooleanField(default=False)
    participation_info = models.TextField(blank=True, null=True)

    # Custom manager
    objects = EventManager()

    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')
        abstract = True

    def __unicode__(self):
        return self.name
