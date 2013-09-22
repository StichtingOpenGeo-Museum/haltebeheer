'''
Import a KV1 dump in TSV format 

@author: Joel Haasnoot
'''
import csv, codecs, logging
from optparse import make_option 

from haltes.utils import file, geo
from haltes.stops import admin # Needed for reversion
from haltes.stops.models import UserStop, BaseStop, StopAttribute, Source, SourceAttribute
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import *
from django import db

import reversion
from os.path import exists, join
from os import listdir

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--delimiter',
            dest='delimiter',
            help='Delimiter to use between fields'),
        )

    def handle(self, *args, **options):
        if (len(args) < 2):
            return self.do_help()

        # Resolve all filenames
        usrstop_filename = None
        usrstar_filename = None
        point_filename = None

        for filename in listdir(args[0]):
            if usrstop_filename is None and filename.lower().startswith('usrstop'):
                usrstop_filename = filename
            
            if usrstar_filename is None and filename.lower().startswith('usrstar'):
                usrstar_filename = filename
            
            if point_filename is None and filename.lower().startswith('point'):
                point_filename = filename
        
        mapping = "usrstop - %s, usrstar - %s and point - %s" % (usrstop_filename, usrstar_filename, point_filename)
        if usrstop_filename is None or usrstar_filename is None or point_filename is None:
            return "Couldn't find all 3 required files (%s)" % mapping 
        else:
            print "Using: %s" % mapping
        
        # Retrieve source - used for encoding    
        source = Source.objects.get(source_id=str(args[1]).lower())
        if source is None:
            return "Couldn't find the specified source - specify a data source"
        
        # 2. Read files
        # Create mapping
        csv.register_dialect('kv1', quotechar='"', 
                             delimiter=(options['delimiter'] if options['delimiter'] is not None else '|'), 
                             doublequote=False, lineterminator='\n', quoting=csv.QUOTE_NONE)
        
        # Read files
        print "Using %s as encoding" % source.encoding
        f1 = codecs.open(join(args[0], usrstop_filename), mode='rU')
        if 'dataownercode' not in f1.readline().lower():
            return "Huston, we have no headers!\n"
        f1.close()
        
        stops = file.UnicodeDictReader(codecs.open(join(args[0], usrstop_filename), mode='rU'), source.encoding, dialect=csv.get_dialect('kv1'))
        stoparea_rows = file.UnicodeDictReader(codecs.open(join(args[0], usrstar_filename), mode='rU'), source.encoding, dialect=csv.get_dialect('kv1'))
        point_rows = file.UnicodeDictReader(codecs.open(join(args[0], point_filename), mode='rU'), source.encoding, dialect=csv.get_dialect('kv1'))             
        
        # Do some translation
        points = { point['PointCode'] : point for point in point_rows if point.get('PointCode', False) }
        areas = { area['UserStopAreaCode'] : area for area in stoparea_rows if area.get('UserStopAreaCode', False) }
        
        print "Doing stops"
        for stop in stops:
            with db.transaction.commit_on_success():
                with reversion.create_revision():
                    if stop.get('TimingPointCode', False):
                        print "Huston, TPC was none, falling back to USC"
                        stop['TimingPointCode'] = stop.get('UserStopCode', False)
                        if stop.get('TimingPointCode', False):
                            return "We had no TPC or USC - import halted"

                    # Figure out our location
                    stop_location = points[stop.get('UserStopCode')]
                    pnt = geo.transform_rd(Point(int(stop_location['LocationX_EW']), int(stop_location['LocationY_NS']), srid=28992))
                    
                    s, created = UserStop.objects.get_or_create(tpc=stop['TimingPointCode'], 
                                                                defaults={u'common_name' : stop['Name'].replace(stop['Town']+', ', ''), 
                                                                          u'common_city' : stop['Town'], 
                                                                          'point' : pnt.wkt })

                    # Check for stop areas
                    if stop['UserStopAreaCode'] is not None and stop['UserStopAreaCode'] in areas:
                        s.parent = self.get_create_star(areas[stop['UserStopAreaCode']], source)
                        s.save()
                        
                    # Save as much as the original data as possible 
                    self.create_source_attr(s, source, 'id', stop['TimingPointCode'])
                    self.create_source_attr(s, source, 'GetIn', stop['GetIn'])
                    self.create_source_attr(s, source, 'GetOut', stop['GetOut'])
                    self.create_source_attr(s, source, 'Name', stop['Name'])
                    self.create_source_attr(s, source, 'Town', stop['Town'])
                    self.create_source_attr(s, source, 'UserStopAreaCode', stop['UserStopAreaCode'])
                    self.create_source_attr(s, source, 'MinimalStopTime', stop['MinimalStopTime'])
                    self.create_source_attr(s, source, 'UserStopType', stop['UserStopType'])
                    self.create_source_attr(s, source, 'latitude', int(stop_location['LocationX_EW']))
                    self.create_source_attr(s, source, 'longitude', int(stop_location['LocationY_NS']))
                    
                    reversion.set_comment("KV1 Import")
        
    def create_source_attr(self, stop, source, key, value):
        self.get_create_update(SourceAttribute, {'stop' : stop, 'source' : source, 'key' : key}, {'value' : value} )
        
    def get_create_update(self, model, get_kwargs, update_values):
        ''' This helper function makes a simple one line update possible '''
        sa, created = model.objects.get_or_create(**get_kwargs);
        for (key, value) in update_values.items():
            setattr(sa, key, value)
        sa.save()
    
    ''' Get or create a stop area to be a parent '''
    def get_create_star(self, stop_area, source):
        attr = BaseStop.objects.filter(sourceattribute__value=stop_area['UserStopAreaCode'], stop_type=2)
        if attr:
            # We're going to assume there's only one of you
            #print "Using an existing star %s" % attr[0]
            sa = attr[0]
        else:
            # Create the stop area, it doesn't exist
            #print "Creating new star %s" % stop_area['Name']
            sa = BaseStop(common_name=stop_area['Name'].replace(stop_area['Town']+', ', ''), 
                        common_city=stop_area['Town'], 
                        stop_type=2)
            sa.save()
        # Make sure the attribute is created
        self.get_create_update(SourceAttribute, {'stop' : sa, 'source' : source, 'key' : u'UserStopAreaCode'}, {'value' : stop_area['UserStopAreaCode']} )
        return sa
      
    def do_help(self):
        print "Not enough parameters or something else bad"
        pass