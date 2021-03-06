from models import UserStop, BaseStop
from forms import SearchForm
from django.shortcuts import render
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.cache import cache_page
import reversion
from django.http import Http404

def home(request):
    return render(request, 'stops/home.html', { 'form': SearchForm() })

def search(request, term = None):
    form = search_term = result_list = results = None
    if request.POST:
        form = SearchForm(request.POST)
        if form.is_valid():
            search_term = form.cleaned_data['terms']
    if term is not None:
        # Note, we might need to do some cleanup here
        search_term = term 
    if search_term is not None:
        # Get results
        result_list = BaseStop.search(search_term)
        
        paginator = Paginator(result_list, 25)
        page = request.GET.get('page', 1)
        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            results = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            results = paginator.page(paginator.num_pages)
    if form is None:
        form = SearchForm()

    return render(request, 'stops/results.html', { 'results' : results, 'term' : search_term, 'form' : form })

# Cache this frontpage often, it's very slow
@cache_page(60 * 15)
def cities(request):
    cities = BaseStop.objects.filter(stop_type=2).values('common_city').annotate(count=Count('common_city')).order_by('common_city')
    return render(request, 'stops/cities.html', { 'cities' : cities})

def city_stops(request, city):
    stops = BaseStop.objects.filter(common_city__iexact=city, stop_type=2).order_by('common_name')
    return render(request, 'stops/stops.html', { 'stops' : stops })

#def stop(request, stop_id=None, tpc=None):
#    if stop_id is not None:
#        stop = UserStop.objects.get(id=stop_id)
#    else:
#        stop = UserStop.objects.get(tpc=tpc)
#    if stop is None:
#        return Http404
#    return render(request, 'stops/stop.html', { 'stop' : stop, 'history' : reversion.get_for_object(stop)})

def stop_json(request, stop_id):
    return render(request, 'stops/stop_json.html', { 'stop' : UserStop.objects.get(id=stop_id) })