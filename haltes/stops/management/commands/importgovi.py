'''
Import a KV1 dump in TSV format 

@author: Joel Haasnoot
'''

import csv, codecs
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from django.contrib.auth.models import User
 
from haltes.utils import file, geo
from haltes.stops.models import BaseStop, UserStop, StopAttribute, Source, SourceAttribute
from haltes.stops import admin # Needed to track reversion

import reversion

class Command(BaseCommand):

    def handle(self, *args, **options):
        if (len(args) < 1):
            return 

        csv.register_dialect('quotescolon', quotechar='"', delimiter=';', doublequote=False, lineterminator='\n', quoting=csv.QUOTE_NONE)
        f = codecs.open(args[0], mode='rU') 
        stops = file.UnicodeDictReader(f, 'utf-8', dialect=csv.get_dialect('quotescolon'))

        with reversion.create_revision(): 
            source, created = Source.objects.get_or_create(source_id=u'govi', defaults={u'name': "GOVI"})          
            for stop in stops:
                split = str(stop['TimingPointName']).split(',')
                if len(split) > 1:
                    city = split[0]
                    name = split[1].lstrip()
                else:
                    city = stop['TimingPointTown'].capitalize()
                    name = stop['TimingPointName']
                point = geo.transform_rd(Point(x=int(stop['LocationX_EW']), y=int(stop['LocationY_NS']), srid=28992))
        
                s, created = UserStop.objects.get_or_create(tpc=stop[u"\ufeffTimingPointCode"], # Don't ask 
                                                            defaults={u'common_name' : name, u'common_city' : city, 'point' : point.wkt})
                
                # Get or create our source
                for attr in stop.keys():
                    self.get_create_update(SourceAttribute, {'stop' : s, 'source' : source, 'key' : attr.capitalize()}, {'value' : stop[attr]} )
                
            reversion.set_comment(u"GOVI Import")
        f.close()
        
    def get_create_update(self, model, get_kwargs, update_values):
        ''' This helper function makes a simple one line update possible '''
        sa, created = model.objects.get_or_create(**get_kwargs);
        for (key, value) in update_values.items():
            setattr(sa, key, value)
        sa.save()