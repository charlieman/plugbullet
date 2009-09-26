from django.conf.urls.defaults import *

urlpatterns = patterns('bullet.views',
    #(r'^bullet/$', 'index'  ),
    (r'^bullet/registrar/$', 'register'),
    (r'^bullet/evento/(.*)/$', 'show_event'),
    (r'^bullet/lista/(\d{4})/(\d{2})/$', 'list'),
    (r'^bullet/calendario/(\d{4})/(\d{2})/$', 'calendar'),
    (r'^bullet/widget/$', 'widget'),
)
