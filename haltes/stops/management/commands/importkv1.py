'''
Import a KV1 dump in TSV format 

@author: Joel Haasnoot
'''

import codecs
import csv
from haltes.stops.models import Stop, StopAttribute, Agency, AgencyAttribute
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import *
from django.utils.datetime_safe import datetime

#import reversion


class Command(BaseCommand):

    def handle(self, *args, **options):
        if (len(args) < 2):
            return self.do_help()
        
        stops = self.open_file(args[0]+"/usrstop.tsv", 3)
        point_rows = self.open_file(args[0]+"/point.tsv", 3)
            
        # Collections of stops
        #stop_area = self.open_file(args[0]+"/usrstar.tsv")
        
        a = Agency.objects.get(name=args[1])
        # Reversions are currently disabled
        #with reversion.create_revision():
        for key in stops:
            stop = stops[key]
            pnt = Point(int(point_rows[key][7]), int(point_rows[key][8]), srid=28992)
            pnt.transform(4326)
            s = Stop(tpc=key,
                     common_name=stop[7].replace(stop[8]+', ', ''),
                     common_city=stop[8],
                     point=pnt)
            s.save()
            
#           StopAttribute(stop=s, key=k, value=j['HALTELIST'][v][i]).save()

            AgencyAttribute(stop=s, agency=a, key='id', value=key).save()   
            AgencyAttribute(stop=s, agency=a, key='GetIn', value=stop[5]).save()
            AgencyAttribute(stop=s, agency=a, key='GetOut', value=stop[6]).save()
            AgencyAttribute(stop=s, agency=a, key='Name', value=stop[7]).save()
            AgencyAttribute(stop=s, agency=a, key='Town', value=stop[8]).save()
            AgencyAttribute(stop=s, agency=a, key='UserStopAreaCode', value=stop[9]).save()
            AgencyAttribute(stop=s, agency=a, key='MinimalStopTime', value=stop[13]).save()
            AgencyAttribute(stop=s, agency=a, key='UserStopType', value=stop[16]).save()
            AgencyAttribute(stop=s, agency=a, key='latitude', value=int(point_rows[key][7])).save()
            AgencyAttribute(stop=s, agency=a, key='longitude', value=int(point_rows[key][8])).save()

            # Import attributes
            StopAttribute(stop=s, key='import_source', value='kv1').save()
            StopAttribute(stop=s, key='import_date', value=datetime.isoformat(datetime.now())).save()
        #reversion.set_comment("Import of agency %s at %s" % (a.name, datetime.datetime.now().isoformat())
        
    def open_file(self, filename, key_column=None):
        f = codecs.open(filename, encoding='utf-8', mode='r')
        i = 0
        output = {}
        for row in f.read().split('\n')[:-1]:
            row = row.split('\t')
            if key_column is None:
                output[i] = row
            else:
                output[row[key_column]] = row
        return output
    
    def do_help(self):
        
        return 1