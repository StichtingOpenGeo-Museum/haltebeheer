'''
Created on Dec 18, 2011
Import a JSON dump
@author: Joel Haasnoot
@author: Stefan de Konink
'''

import codecs, csv
import simplejson as json
from django.contrib.gis.geos import *
from django.core.management.base import BaseCommand

from haltes.stops.models import UserStop, StopAttribute, Source, SourceAttribute
from haltes.stops import admin # Needed to track reversion

import reversion

class Command(BaseCommand):

    def UnicodeDictReader(self, str_data, encoding, **kwargs):
        csv_reader = csv.DictReader(str_data, **kwargs)
        # Decode the keys once
        keymap = dict((k, k.decode(encoding)) for k in csv_reader.fieldnames)
        for row in csv_reader:
            yield dict((keymap[k], unicode(v, 'utf-8')) for k, v in row.iteritems())

    def handle(self, *args, **options):
        f = open(args[0], mode='r') #codecs.open(args[0], encoding='utf-8', mode='r')
        reader = self.UnicodeDictReader(f, 'utf-8', dialect=csv.excel)
        
        # Get or create our source
        source, created = Source.objects.get_or_create(source_id=u'cxx', defaults={u'name': "Connexxion Website"})
        
        #Loop over stops
        with reversion.create_revision(): 
            for row in reader:
                common_city = row['naam'].replace(', '+row['kortenaam'], '')
                pnt = Point(int(row['longitude'])/10000000.0,
                            int(row['latitude'])/10000000.0, srid=4326)
                
                s, created = UserStop.objects.get_or_create(tpc=row['code'], 
                                                        defaults={u'common_name' : row['kortenaam'], u'common_city' : common_city, 'point' : pnt })
                
                self.get_create_update(StopAttribute, {'stop' : s, 'key' : u"Zone"}, {'value' : row['zone']})
                
                for agency_attr in row.keys():
                    self.get_create_update(SourceAttribute, {'stop' : s, 'source' : source, 'key' : agency_attr.capitalize()}, {'value' : row[agency_attr]} )
            
            reversion.set_comment(u"Connexxion Import")
        f.close()
        
    def get_create_update(self, model, get_kwargs, update_values):
        ''' This helper function makes a simple one line update possible '''
        sa, created = model.objects.get_or_create(**get_kwargs);
        for (key, value) in update_values.items():
            setattr(sa, key, value)
        sa.save()