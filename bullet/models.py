from django.db import models
from datetime import datetime
from random import randint

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models import Q

import bullet.constants as constants

class Bullet(models.Model):
    pass

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
    url = models.URLField(verify_exists=False)

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
        return '%s <%s>' % (self.sender_name, self.sender_email)

class TwitterChannel(models.Model):
    access_token_key = models.CharField(max_length=256, blank=True)
    access_token_secret = models.CharField(max_length=256, blank=True)

    class Meta:
        verbose_name = _('twitter channel')
        verbose_name_plural = _('twitter channels')

    def __unicode__(self):
        return self.name

class Bulletin(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    description = models.TextField()
    email_channels = models.ManyToManyField(EmailChannel, null=True, blank=True)
    email_enabled = models.BooleanField(default=True)
    twitter_channels = models.ManyToManyField(TwitterChannel, null=True, blank=True)
    twitter_enabled = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, related_name="related_user") #, editable=False)
    organization = models.ForeignKey(Organization)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('bulletin')
        verbose_name_plural = _('bulletins')

    def __unicode__(self):
        return self.name

    def save(self, force_insert=False, force_update=False):
        #self.submissions_related = #username
        super(Bulletin, self).save(force_insert, force_update) # Call the "real" save() method.

class BulletinEdition(models.Model):
    name = models.CharField(max_length = 128)
    slug = models.SlugField(max_length = 128)
    description = models.TextField()
    bulletin = models.ForeignKey(Bulletin, related_name='editions')
    delivery_ts = models.DateTimeField(blank=True, null=True)
    delivered = models.BooleanField(default=False)
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    submission_period_start = models.DateTimeField()
    submission_period_end = models.DateTimeField()
    created_by = models.ForeignKey(User, related_name="submissions")#, editable=False)
    organization = models.ForeignKey(Organization)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('bulletin')
        verbose_name_plural = _('bulletins')

    def __unicode__(self):
        return self.name


class SubmissionManager(models.Manager):
    pass

class Submission(models.Model):
    title = models.CharField(max_length = 128)
    body = models.TextField()
    url = models.URLField(verify_exists=False)
    submitted_by = models.ForeignKey(User, related_name="%(class)s_related")#, editable=False)
    organization = models.ForeignKey(Organization)
    status = models.PositiveIntegerField(choices=constants.SUBMISSION_STATUS_CHOICES)
    editions = models.ManyToManyField(BulletinEdition)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    # Custom manager
    objects = SubmissionManager()

    class Meta:
        verbose_name = _('Submission')
        verbose_name_plural = _('Submissions')
        abstract = True

    def __unicode__(self):
        return self.title

class EventManager(models.Manager):

    def month_events(self, year=None, month=None, from_today=None):
        """Retrieves events for given month
        set from_today=True for retrieving this months events from today
        until the end of the month"""
        today = datetime.now().replace(hour=0, minute=0)

        year = year or today.year
        month = month or today.month

        if from_today:
            first_day = today
        else:
            first_day = today.replace(day=1)

        if first_day.month == 12:
            last_day = first_day.replace(year=first_day.year + 1, month=1)
        else:
            last_day = first_day.replace(month=first_day.month + 1)

        return self.filter(
                    Q(start_ts__gte=first_day) | Q(end_ts__lt=last_day),
                    status=constants.SUBMISSION_STATUS_ACCEPTED
                ).order_by('start_ts')

    def comming_soon(self, exclude=None):
        """Retrieves a random event with probability based on
        date closeness (weight)"""
        # TODO: return several events based on a limit parameter

        # only show events since today
        events = self.month_events(from_today=True)

        if exclude:
            events = events.exclude(id=exclude.id)

        today = datetime.now().replace(hour=0, minute=0)

        # This will give you a number -a weight- based on the distance
        # of the day from today.
        # if today is 10 and it starts 15 then weight = 31 - (15 - 10) = 26
        # if today is 15 and it started 13 and ends 17 then
        # weight = 31 - (17 - 15) = 29
        # if today is 2 and it starts 20 then weight = 31 - (20 - 2) = 13
        # TODO: give even more weight to events happening right today,
        #       in the next 2 days and next 7 days
        weight = []
        for event in events:
            if event.start_ts > today:
                value = event.start_ts
            else:
                value = event.end_ts
            #value = event.start_ts if event.start_ts > today else event.end_ts
            value = (value - today).days
            value = 31 - value
            weight.append(value)
            
        #weight = [31 - ((ev.start_ts if ev.start_ts > today else ev.end_ts) - today).days for ev in result]
        lowest = min(weight)
        total = sum(weight)

        # maybe should use izip for optimization?
        # from itertools import izip
        data = zip(weight, events)
        data.sort()

        overweight = 0
        n = randint(lowest, total)

        result = None
        for weight, event in data:
            overweight += weight
            if overweight >= n - 1:
                result = event
                break

        return result


class Event(Submission):

    start_ts = models.DateTimeField()
    end_ts = models.DateTimeField()
    paid = models.BooleanField(default=False)
    participation_info = models.TextField(blank=True, null=True)

    # Custom manager
    objects = EventManager()

    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')
        #abstract = True

    def __unicode__(self):
        return self.title
