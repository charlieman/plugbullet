from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import redirect_to
from plugbullet.main_site.views import main_page


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #(r'^hello/$', 'views.hello'),
    (r'^bullet/', include('plugbullet.bullet.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    #(r'.*', include('plugbullet.main_site.urls')),
    #(r'^$', main_page),
    #(r'^$', redirect_to, {'url': '/main/'}),
    #(r'^main/', include('plugbullet.main_site.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )

urlpatterns += patterns('',
    (r'^', include('plugbullet.main_site.urls')),
)
