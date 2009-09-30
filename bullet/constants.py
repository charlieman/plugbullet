#-*- coding: utf-8 -*-
from django.utils.translation import ugettext as _

STATUS_SENT     = 0
STATUS_EVAL     = 1
STATUS_ACCEPTED = 2
STATUS_OBSERVED = 3
STATUS_REJECTED = 4

STATUS_CHOICES = (
    (STATUS_SENT,     _(u'Enviado')),
    (STATUS_EVAL,     _(u'Evaluación')),
    (STATUS_ACCEPTED, _(u'Aceptado')),
    (STATUS_OBSERVED, _(u'Observado')),
    (STATUS_REJECTED, _(u'Rechazado')),
)
