'''
Import a KV1 dump in TSV format 

@author: Joel Haasnoot
'''

from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from django.contrib.auth.models import User
 
from haltes.utils import file, geo
from haltes.stops.models import BaseStop, UserStop, StopAttribute, Agency, SourceAttribute

import reversion
from haltes.stops import admin # Needed to track reversion

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
            
                    s, created = UserStop.objects.get_or_create(tpc=stop[0], 
                                                                defaults={u'common_name' : name, u'common_city' : city, 'point' : point.wkt})
                    s.save()
            reversion.set_comment(u"GOVI Import")