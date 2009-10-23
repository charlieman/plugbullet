from django import forms
from django.utils.translation import ugettext_lazy as _

class EventRegistrationForm(forms.Form):
    title = forms.CharField(max_length=30, label=_(u'Title'))
    body = forms.CharField(label=_(u'Content'), widget=forms.widgets.Textarea())

