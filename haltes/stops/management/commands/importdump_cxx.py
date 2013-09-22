'''
Created on Dec 18, 2011
Import a JSON dump
@author: Joel Haasnoot
@author: Stefan de Konink
'''

import time, codecs, csv
import simplejson as json
from django.contrib.gis.geos import *
from django import db
from django.core.management.base import BaseCommand

from haltes.stops.models import UserStop, StopAttribute, Source, SourceAttribute
from haltes.stops import admin # Needed to track reversion
from haltes.utils import file

import reversion

class Command(BaseCommand):

    def handle(self, *args, **options):
        t0 = time.time()
        f = open(args[0], mode='r') #codecs.open(args[0], encoding='utf-8', mode='r')
        reader = file.UnicodeCsvReader(f, 'utf-8', dialect=csv.excel)
        
        # Get or create our source
        source, created = Source.objects.get_or_create(source_id=u'cxx', defaults={u'name': "Connexxion Website"})
        keymap = False
        #Loop over stops
        for row in reader:
            if not keymap:
                keymap = row
            else:       
                with db.transaction.commit_on_success(): 
                    with reversion.create_revision():
                        common_city = row[4].replace(', '+row[7], '')
                        pnt = Point(int(row[8])/10000000.0,
                                    int(row[6])/10000000.0, srid=4326)
                        
                        s, created = UserStop.objects.get_or_create(tpc=row[1], 
                                                                defaults={u'common_name' : row[7], u'common_city' : common_city, 'point' : pnt })
                        
                        self.get_create_update(StopAttribute, {'stop' : s, 'key' : u"Zone"}, {'value' : row[2]})
                        
                        i = 0
                        for agency_attr in row:
                            self.get_create_update(SourceAttribute, {'stop' : s, 'source' : source, 'key' : unicode(keymap[i]).capitalize()}, {'value' : row[i]} )
                            i += 1
                    
                        reversion.set_comment(u"Connexxion Import")
        f.close()
        print "Executed in "+str(time.time()-t0)+ " seconds"
        
    def get_create_update(self, model, get_kwargs, update_values):
        ''' This helper function makes a simple one line update possible '''
        sa, created = model.objects.get_or_create(**get_kwargs);
        for (key, value) in update_values.items():
            setattr(sa, key, value)
        sa.save()