from django.conf.urls.defaults import patterns, include, url
from django.contrib.gis import admin
from django.views.generic.detail import DetailView

from stops.models import BaseStop, UserStop

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'stops.views.home', name='home'),
    url(r'^cities/?$', 'stops.views.cities', name='cities'),
    url(r'^search/(?P<term>[\w]+)?/?$', 'stops.views.search', name='search'),
    # \w .,-/\(\)\'\`]
    url(r'^stops/(?P<city>.+)/?$', 'stops.views.city_stops', name='city_stops'),
    url(r'^stop/(?P<pk>[\d]+)/?$', DetailView.as_view(model=BaseStop), name='stop'),
    url(r'^stop/tpc/(?P<tpc>[\d]{0,8})/?$', DetailView.as_view(model=UserStop, slug_field='tpc', slug_url_kwarg='tpc'), name='stop_tpc'),
    url(r'^stop/(?P<stop_id>[\w]+)/json/?$', 'stops.views.stop_json', name='stop_json'),
    
    (r'^admin/', include(admin.site.urls)),
)
