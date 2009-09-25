from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^bullet/registrar/$', registrar),
    (r'^bullet/evento/(.*)/$', evento_unico),
    (r'^bullet/lista/(.*)/$', lista),
    (r'^bullet/calendario/(\d{4})/(\d{2})/$', calendario),
    (r'^bullet/widget/$', widget),
    (r'^bullet/$', registrar),
)
