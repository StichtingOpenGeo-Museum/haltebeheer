'''
Import a KV1 dump in TSV format 

@author: Joel Haasnoot
'''

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

        stops = file.open_file_list(args[0], delimeter=';', cr='\r')

        with reversion.create_revision():           
            for stop in stops[1:]: # Skip the headers
                split = str(stop[1]).split(',')
                if len(split) > 1:
                    city = split[0]
                    name = split[1].lstrip()
                else:
                    city = stop[2].capitalize()
                    name = stop[1]
                point = geo.transform_rd(Point(x=int(stop[3]), y=int(stop[4]), srid=28992))
        
                s, created = UserStop.objects.get_or_create(tpc=stop[0], 
                                                            defaults={u'common_name' : name, u'common_city' : city, 'point' : point.wkt})
                
                # Get or create our source
                source, created = Source.objects.get_or_create(source_id=u'govi', defaults={u'name': "GOVI"})
                self.get_create_update(SourceAttribute, {'stop' : s, 'source' : source, 'key' : u'TimingPointCode'}, {'value' : stop[0]} )
                self.get_create_update(SourceAttribute, {'stop' : s, 'source' : source, 'key' : u'TimingPointName'}, {'value' : stop[1]} )
                self.get_create_update(SourceAttribute, {'stop' : s, 'source' : source, 'key' : u'TimingPointTown'}, {'value' : stop[2]} )
                self.get_create_update(SourceAttribute, {'stop' : s, 'source' : source, 'key' : u'LocationX_EW'}, {'value' : stop[3]} )
                self.get_create_update(SourceAttribute, {'stop' : s, 'source' : source, 'key' : u'LocationY_NS'}, {'value' : stop[4]} )
                
            reversion.set_comment(u"GOVI Import")
            
    def get_create_update(self, model, get_kwargs, update_values):
        ''' This helper function makes a simple one line update possible '''
        sa, created = model.objects.get_or_create(**get_kwargs);
        for (key, value) in update_values.items():
            setattr(sa, key, value)
        sa.save()