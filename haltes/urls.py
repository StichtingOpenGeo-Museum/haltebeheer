from django.conf.urls.defaults import patterns, include, url
from django.contrib.gis import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'stops.views.home', name='home'),
    url(r'^cities/?$', 'stops.views.cities', name='cities'),
    url(r'^search/?$', 'stops.views.search', name='search'),
    # \w .,-/\(\)\'\`]
    url(r'^stops/(?P<city>.+)/?$', 'stops.views.city_stops', name='city_stops'),
    url(r'^stop/(?P<id>[\w]+)/?$', 'stops.views.stop', name='stop'),
    url(r'^stop/(?P<id>[\w]+)/json/?$', 'stops.views.stop_json', name='stop_json'),
    
    (r'^admin/', include(admin.site.urls)),
)
