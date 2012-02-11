'''
Import a KV1 dump in TSV format 

@author: Joel Haasnoot
'''

from haltes.utils import file, geo
from haltes.stops import admin # Needed for reversion
from haltes.stops.models import UserStop, BaseStop, StopAttribute, Source, SourceAttribute
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import *
from django import db

import reversion


class Command(BaseCommand):

    def handle(self, *args, **options):
        if (len(args) < 2):
            return self.do_help()
        
        stops = file.open_file_dict(args[0]+"/usrstop.tsv", 3)
        point_rows = file.open_file_dict(args[0]+"/point.tsv", 3)
            
        # Collections of stops
        stop_area = file.open_file_dict(args[0]+"/usrstar.tsv", 3)
        
        # TODO: Fix this to actually look at the first field
        source = Source.objects.get(source_id=str(args[1]).lower())
        
        for key in stops:
            with db.transaction.commit_on_success():
                with reversion.create_revision():
                    stop = stops[key]
                    pnt = geo.transform_rd(Point(int(point_rows[key][7]), int(point_rows[key][8]), srid=28992))
                    
                    s, created = UserStop.objects.get_or_create(tpc=key, 
                                                                defaults={u'common_name' : stop[7].replace(stop[8]+', ', ''), 
                                                                          u'common_city' : stop[8], 
                                                                          'point' : pnt.wkt })
                    
                    # Check for stop areas
                    if stop[9] is not None and stop[9] in stop_area:
                        s.parent = self.get_create_star(stop_area[stop[9]], source)
                        s.save()
         
                    # Save as much as the original data as possible 
                    self.get_create_update(SourceAttribute, {'stop' : s, 'source' : source, 'key' : 'id'}, {'value' : key} )
                    self.get_create_update(SourceAttribute, {'stop' : s, 'source' : source, 'key' : 'GetIn'}, {'value' : stop[5]} )
                    self.get_create_update(SourceAttribute, {'stop' : s, 'source' : source, 'key' : 'GetOut'}, {'value' : stop[6]} )
                    self.get_create_update(SourceAttribute, {'stop' : s, 'source' : source, 'key' : 'Name'}, {'value' : stop[7]} )
                    self.get_create_update(SourceAttribute, {'stop' : s, 'source' : source, 'key' : 'Town'}, {'value' : stop[8]} )
                    self.get_create_update(SourceAttribute, {'stop' : s, 'source' : source, 'key' : 'UserStopAreaCode'}, {'value' : stop[9]} )
                    self.get_create_update(SourceAttribute, {'stop' : s, 'source' : source, 'key' : 'MinimalStopTime'}, {'value' : stop[13]} )
                    self.get_create_update(SourceAttribute, {'stop' : s, 'source' : source, 'key' : 'UserStopType'}, {'value' : stop[16]} )
                    self.get_create_update(SourceAttribute, {'stop' : s, 'source' : source, 'key' : 'latitude'}, {'value' : int(point_rows[key][7])} )
                    self.get_create_update(SourceAttribute, {'stop' : s, 'source' : source, 'key' : 'longitude'}, {'value' : int(point_rows[key][8])} )
                    
                    reversion.set_comment("KV1 Import")
        
    def get_create_update(self, model, get_kwargs, update_values):
        ''' This helper function makes a simple one line update possible '''
        sa, created = model.objects.get_or_create(**get_kwargs);
        for (key, value) in update_values.items():
            setattr(sa, key, value)
        sa.save()
    
    ''' Get or create a stop area to be a parent '''
    def get_create_star(self, stop_area, source):
        attr = BaseStop.objects.filter(sourceattribute__value=stop_area[3], stop_type=2)
        if attr:
            # We're going to assume there's only one of you
            sa = attr[0]
        else:
            # Create the stop area, it doesn't exist
            sa = BaseStop(common_name=stop_area[4].replace(stop_area[5]+', ', ''), 
                        common_city=stop_area[5], 
                        stop_type=2)
            sa.save()
        # Make sure the attribute is created
        self.get_create_update(SourceAttribute, {'stop' : sa, 'source' : source, 'key' : u'UserStopAreaCode'}, {'value' : stop_area[3]} )
        return sa
