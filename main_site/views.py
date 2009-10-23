from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import logout

def main_page(request):
    variables = RequestContext(request, {
    })
    return render_to_response('main_site/main_page.html', variables)
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

