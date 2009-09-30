from django.conf.urls.defaults import *
from django.views.generic.date_based import archive_month

urlpatterns = patterns('bullet.views',
    #(r'^bullet/$', 'index'  ),
    (r'^registrar/$', 'register'),
    (r'^evento/(.*)/$', 'show_event'),

    url(r'^list/(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
        archive_month,
        {'template': 'bullet/list.html', 'date_field': 'start_date'},
        name='bullet-list'),

    url(r'^calendar/(?P<year>\d{4})/(?P<month>\w{3})/$',
        archive_month,
        {'template': 'bullet/calendar.html'},
        name='bullet-calendar'),

    (r'^widget/$', 'widget'),
)
