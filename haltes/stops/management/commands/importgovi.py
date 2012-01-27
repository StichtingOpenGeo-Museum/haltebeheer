'''
Import a KV1 dump in TSV format 

@author: Joel Haasnoot
'''

from haltes.stops import admin # Needed to track reversion 
from haltes.utils import file, geo
from haltes.stops.models import Stop, StopAttribute, Agency, SourceAttribute
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from django.utils.datetime_safe import datetime
from django.contrib.auth.models import User
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
                point = Point(x=stop[3], y=stop[4], srid=28992)
                point = geo.transform_rd(point)
                
                s, created = Stop.objects.get_or_create(tpc=stop[0], defaults={'common_name' : name, 'common_city' : city})
                if created: # Only change the location if created
                    s.point = point
                    s.save()
                # TODO: Add logic here related to detecting location changes
    
#                a = StopAttribute.objects.get_or_create(stop=s, key='type')
#                if a.value != stop[4]:
#                    a.value = 
#                StopAttribute.objects.get_or_create(stop=s, key='import_source', value='govi').save()
#                StopAttribute.objects.get_or_create(stop=s, key='import_date', value=datetime.isoformat(datetime.now())).save()
            reversion.set_comment(u"GOVI Import")