#-*- coding: utf-8 -*-
# Create your views here.
from django.views.generic.simple import direct_to_template
from models import Bullet

def index():
    pass

def register():
    pass

def show_event():
    pass

def list(year, day):
    pass

def calendar(year, day):
    pass

def widget():
    pass

# helper functions

def filterls(locals):
    """Use this to directly pull local variables from locals() in the view
    to the template while strip unwanted variables (those that start with
    '_'), like this:
    return render_to_response('some_template.html', filterls(locals()))
    """
    for var in locals.keys():
        if var.startswith("_"): del locals[var]
    return locals
