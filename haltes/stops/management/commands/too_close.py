from django.core.management.base import BaseCommand
from django.contrib.gis.measure import D
from haltes.stops.models import UserStop, StopAttribute, Source, SourceAttribute

class Command(BaseCommand):

    def handle(self, *args, **options):
        if len(args) == 1:
            radius_distance = args[0]
        else:
            radius_distance = 1.5
            
        close_list = []
        for stop in UserStop.objects.filter():
            too_close = UserStop.objects.filter(point__distance_lte=(stop.point.wkt, D(m=radius_distance)))
            for close in too_close:
                tuple = (stop.tpc, close.tpc)
                if tuple not in close_list and (close.tpc, stop.tpc) not in close_list and stop.tpc != close.tpc:
                    close_list.append(tuple)
        
        # Now print the list
        for item in close_list:
            print item[0]+","+item[1]
        