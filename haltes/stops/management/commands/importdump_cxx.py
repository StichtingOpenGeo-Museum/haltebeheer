'''
Created on Dec 18, 2011
Import a JSON dump
@author: Joel Haasnoot
@author: Stefan de Konink
'''

import codecs
import simplejson as json
from haltes.stops.models import Stop, StopAttribute, Agency, AgencyAttribute
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import *

class Command(BaseCommand):

    def handle(self, *args, **options):
        f = codecs.open(args[0], encoding='utf-8', mode='r') 
        content = f.read()
        f.close()
        content = '{'+content.split('>{')[1].split('}<')[0]+'}'
        j = json.loads(content)
    
        agencies = Agency.objects.filter(name='Connexxion')
        if len(agencies):
            a = agencies[0]
        else:
            a = Agency(name="Connexxion", agency_id="CXX", tz="Europe/Amsterdam", url="www.connexxion.nl")
            a.save()
        for i in range(1, len(j['HALTELIST']['ID'])):
            common_city = j['HALTELIST']['NAAM'][i].replace(', '+j['HALTELIST']['KORTENAAM'][i], '')
            pnt = Point(j['HALTELIST']['LONGITUDE'][i]/10000000.0,
                        j['HALTELIST']['LATITUDE'][i]/10000000.0, srid=4326)
            
            s = Stop(tpc=j['HALTELIST']['ID'][i],
                     common_name=j['HALTELIST']['KORTENAAM'][i],
                     common_city=common_city,
                     point=pnt)
            s.save()
            
            for k, v in {'zone': 'ZONE'}.items():
                StopAttribute(stop=s, key=k, value=j['HALTELIST'][v][i]).save()
            
            for agency_attr in ['ID', 'KORTENAAM', 'CODE', 'ZONE', 'NAAM', 'TONEN', 'BRUGWACHTER', 'LONGITUDE', 'LATITUDE']:
                AgencyAttribute(stop=s, agency=a, key=agency_attr.lower(), value=j['HALTELIST'][agency_attr][i]).save()