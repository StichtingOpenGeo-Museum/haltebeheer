from haltes.batch.check import ErrorCheck
from django.contrib.gis.measure import D
from haltes.stops.models import UserStop, StopAttribute, Source, SourceAttribute
from haltes.batch.models import Error 

class Check(ErrorCheck):
    radius_distance = 1.5
    
    def run(self):
        close_list = []
        for stop in UserStop.objects.filter():
            too_close = UserStop.objects.filter(point__distance_lte=(stop.point.wkt, D(m=self.radius_distance)))
            for close in too_close:
                error = (stop.id, close.id)
                if error not in close_list and (close.id, stop.id) not in close_list and stop.id != close.id:
                    close_list.append(error)
        print len(close_list)
        e = None
        for error in close_list:
            e = Error(severity=2, code='CLOSE')
            e.save()
            for stop in error:
                e.affects.add(UserStop.objects.get(id=stop))
            e.save()
            
        return '%s errors added\n' % len(close_list)    
            