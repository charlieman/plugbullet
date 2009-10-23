from django.conf.urls.defaults import *
from django.utils.translation import ugettext as _

urlpatterns = patterns('main_site.views',
    (r'^$', 'main_page'),
    url(r'^%s/$' % _('logout'), 'logout_page', name='logout'),
)
urlpatterns += patterns('',
    (r'^login/$', 'django.contrib.auth.views.login'),
)
