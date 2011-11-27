import os
from django.contrib.gis.geos import *
from models import Stop, StopAttribute, Agency, AgencyAttribute

def run(verbose=True):
    stops = []
    a = Agency.objects.filter(id=1)
    for stop in stops:
        pnt = Point(954158.1, 4215137.1, srid=32140) # Fix this, change coordinate system
        s = Stop(common_name="", common_city = "", point=pnt)
        s.save()
        for attr in stop.attributes:
            StopAttribute(stop=s, key="", value="").save()
        for agency_attr in stop.attributes:
            AgencyAttribute(stop=s, agency=a, key="", value="").save()