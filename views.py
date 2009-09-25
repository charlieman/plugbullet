from django.http import HttpResponse, Http404
import datetime

# some hello world stuff

def hello(request):
    return HttpResponse("Hello world")


def current_time(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    time = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>%s</body></html>" % time
    return HttpResponse(html)


def the_time(request):
    return current_time(request, -5)

def registrar(request):
    pass

def evento_unico(request):
    pass
def lista(request):
    pass
def calendario(request):
    pass
def widget(request):
    pass

