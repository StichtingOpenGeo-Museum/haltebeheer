# Create your views here.

from models import Stop
from django.shortcuts import render
from django.db.models import Count
from revisions.models import VersionedModel

def cities(request):
    cities = Stop.objects.values('common_city').annotate(count=Count('common_city')).order_by('-count')
    
    return render(request, 'stops/cities.html', { 'cities' : cities})

def city_stops(request, city):
    stops = Stop.objects.all().filter(common_city__iexact=city)
    rev = stops[0].get_revisions()
    return render(request, 'stops/stops.html', { 'stops' : stops, 'rev' : rev })

def stop(request, id):
    stop = Stop.objects.get(id=id).get_latest_revision()
    return render(request, 'stops/stop.html', { 'stop' : stop })