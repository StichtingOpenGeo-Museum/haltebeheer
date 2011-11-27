import os
from models import Stop, StopAttribute

def run(verbose=True):
    stops = []
    for stop in stops:
        s = Stop(common_name="", common_city = "")
        s.save()
        for attr in stop.attributes:
            StopAttribute(stop=s, key="", value="").save()
