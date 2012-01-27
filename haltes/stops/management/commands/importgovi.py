'''
Import a KV1 dump in TSV format 

@author: Joel Haasnoot
'''

from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point

from haltes.stops import admin # Needed to track reversion 
from haltes.utils import file, geo
from haltes.stops.models import BaseStop, StopAttribute, Agency, SourceAttribute

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
                    name = split[1]
                else:
                    city = stop[2].capitalize()
                    name = stop[1]
                point = geo.transform_rd(Point(x=int(stop[3]), y=int(stop[4]), srid=28992))
                
                s, created = BaseStop.objects.get_or_create(tpc=stop[0], defaults={'common_name' : name, 'common_city' : city})
                s.point = point.wkt
                s.save()
                # TODO: Add logic here related to detecting location changes
    
#                StopAttribute.objects.get_or_create(stop=s, key='type').update(value=stop[4)
#                if a.value != stop[4]:
#                    a.value = 
#                StopAttribute.objects.get_or_create(stop=s, key='import_source', value='govi').save()
#                StopAttribute.objects.get_or_create(stop=s, key='import_date', value=datetime.isoformat(datetime.now())).save()
            reversion.set_comment(u"GOVI Import")