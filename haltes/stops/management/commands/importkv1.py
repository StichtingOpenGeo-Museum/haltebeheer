'''
Import a KV1 dump in TSV format 

@author: Joel Haasnoot
'''

from haltes.utils import file, geo
from haltes.stops import admin # Needed for reversion
from haltes.stops.models import BaseStop, StopAttribute, Agency, SourceAttribute
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import *
from django.utils.datetime_safe import datetime

import reversion


class Command(BaseCommand):

    def handle(self, *args, **options):
        if (len(args) < 2):
            return self.do_help()
        
        stops = self.open_file(args[0]+"/usrstop.tsv", 3)
        point_rows = self.open_file(args[0]+"/point.tsv", 3)
            
        # Collections of stops
        stop_area = file.open_file_dict(args[0]+"/usrstar.tsv", 3)
        
        # TODO: Fix this to actually look at the first field
        a = Agency.objects.get(name=args[1])
        # Reversions are currently disabled
        with reversion.create_revision():
            for key in stops:
                stop = stops[key]
                pnt = geo.transform_rd(Point(int(point_rows[key][7]), int(point_rows[key][8]), srid=28992))
                s = BaseStop(tpc=key,
                         common_name=stop[7].replace(stop[8]+', ', ''),
                         common_city=stop[8],
                         point=pnt.wkt)
                s.save()
                
                # Check for stop areas
                if stop[9] is not None and stop[9] in stop_area:
                    s.parent = self.find_create_star(stop_area[stop[9]])                
    
                # Save as much as the original data as possible 
                SourceAttribute(stop=s, agency=a, key='id', value=key).save()   
                SourceAttribute(stop=s, agency=a, key='GetIn', value=stop[5]).save()
                SourceAttribute(stop=s, agency=a, key='GetOut', value=stop[6]).save()
                SourceAttribute(stop=s, agency=a, key='Name', value=stop[7]).save()
                SourceAttribute(stop=s, agency=a, key='Town', value=stop[8]).save()
                SourceAttribute(stop=s, agency=a, key='UserStopAreaCode', value=stop[9]).save()
                SourceAttribute(stop=s, agency=a, key='MinimalStopTime', value=stop[13]).save()
                SourceAttribute(stop=s, agency=a, key='UserStopType', value=stop[16]).save()
                SourceAttribute(stop=s, agency=a, key='latitude', value=int(point_rows[key][7])).save()
                SourceAttribute(stop=s, agency=a, key='longitude', value=int(point_rows[key][8])).save()
    
                # Import attributes
                StopAttribute(stop=s, key='import_source', value='kv1').save()
                StopAttribute(stop=s, key='import_date', value=datetime.isoformat(datetime.now())).save()
            reversion.set_comment("KV1 Import")
        
    def find_create_star(self, stop_area):
        '''Find or create a stop area record'''
        stops = BaseStop.objects.filter(stop_type=2, stopattribute__value=stop_area[4])
        if len(stops):
            # We're going to assume there's only one of you
            return stops[0] 
        else:
            # Create the stop area
            s = BaseStop(common_name=stop_area[5].replace(stop_area[6]+', ', ''), 
                        common_city=stop_area[6], 
                        stop_type=2)
            s.save()
            StopAttribute(stop=s, key='UserStopAreaCode', value=stop_area[4])
            StopAttribute(stop=s, key='import_source', value='kv1').save()
            StopAttribute(stop=s, key='import_date', value=datetime.isoformat(datetime.now())).save()
            return s
    
    def do_help(self):
        
        return 1