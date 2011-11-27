from django.conf.urls.defaults import patterns, include, url
from django.contrib.gis import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'stops.views.cities', name='cities'),
    url(r'^stops/(?P<city>\w+)/?$', 'stops.views.city_stops', name='city_stops'),
    url(r'^stop/(?P<id>\w+)/?$', 'stops.views.stop', name='city_stops'),
    
    (r'^admin/', include(admin.site.urls)),
)
