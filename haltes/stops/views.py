from models import Stop
from forms import SearchForm
from django.shortcuts import render
from django.db.models import Count
from django.views.decorators.cache import cache_page

def home(request):
    return render(request, 'stops/home.html', { 'form': SearchForm() })

def search(request):
    if request.POST:
        form = SearchForm(request.POST)
        if form.is_valid():
            results = Stop.search(form.cleaned_data['terms'])
    form = SearchForm()
    return render(request, 'stops/results.html', 
                  { 'results' : (results if results else []), 'form' : form })

# Cache this frontpage often, it's very slow
@cache_page(60 * 15)
def cities(request):
    cities = Stop.objects.values('common_city').annotate(count=Count('common_city')).order_by('common_city')
    return render(request, 'stops/cities.html', { 'cities' : cities})

def city_stops(request, city):
    stops = Stop.objects.filter(common_city__iexact=city).order_by('common_name')
    return render(request, 'stops/stops.html', { 'stops' : stops })

def stop(request, id):
    stop = Stop.objects.get(id=id)
    return render(request, 'stops/stop.html', { 'stop' : stop })

def stop_json(request, id):
    return render(request, 'stops/stop_json.html', { 'stop' : Stop.objects.get(id=id) })