import os
from django.contrib.gis.geos import *
from models import Stop, StopAttribute, Agency, AgencyAttribute

def run(verbose=True):
    stops = []
    a = Agency.objects.filter(id=1)
    for stop in stops:
        pnt = Point(50, 5, srid=4326) # Fix this, change coordinate system
        s = Stop(common_name="", common_city = "", point=pnt)
        s.save()
        for attr in stop.attributes:
            StopAttribute(stop=s, key="", value="").save()
        for agency_attr in stop.attributes:
            AgencyAttribute(stop=s, agency=a, key="", value="").save()