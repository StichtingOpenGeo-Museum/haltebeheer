import codecs
import simplejson as json
from django.contrib.gis.geos import *
from models import Stop, StopAttribute, Agency, AgencyAttribute

def run(file, verbose=True):
    f = codecs.open(file, encoding='utf-8', mode='r')
    content = f.read()
    f.close()
    content = '{'+content.split('>{')[1].split('}<')[0]+'}'
    j = json.loads(content)

    a = Agency.objects.get(name='Connexxion')
    for i in range(1, len(j['HALTELIST']['ID'])):
        if i / 10000 == 1:
            print "Processed %s" % i
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
