#-*- coding: utf-8 -*-
# Create your views here.
from django.http import HttpResponse
from django.views.generic.simple import direct_to_template
from django.shortcuts import render_to_response
from django.template import RequestContext
from bullet import models
from bullet.forms import EventRegistrationForm

def event_list(request):
    events = models.Event.objects.month_events(from_today=True)
    variables = {
        'events': events,
    }
    return render_to_response('bullet/events_list.html', variables)

def create(request):
    if request.method == 'POST':
        form = EventRegistrationForm(data=request.POST)
    form = EventRegistrationForm()
    variables = {
        'form': form,
    }
    return render_to_response('bullet/create.html', variables)

def show_event(request):
    pass

def list(request, year, day):
    pass

def calendar(request, year, day):
    pass

def direct_json(request):
    from django.core import serializers
    objects = models.Event.objects.month_events(from_today=True)
    json = serializers.serialize('json', objects, ensure_ascii=False)
    json = 'printWidget(%s);' % json
    return HttpResponse(json, mimetype='text/javascript')

def widget(request, template='bullet/iframe.html'):
    events = models.Event.objects.month_events(from_today=True)
    variables = {
        'events': events,
    }
    return render_to_response(template, variables)

# helper functions

def _filterls(locals):
    """Use this to directly pull local variables from locals() in the view
    to the template while strip unwanted variables (those that start with
    '_'), like this:
    return render_to_response('some_template.html', filterls(locals()))
    """
    for var in locals.keys():
        if var.startswith("_"): del locals[var]
    return locals
