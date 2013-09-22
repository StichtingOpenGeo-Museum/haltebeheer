from django.db import models
from django.contrib.gis.db import models as gis_models
import reversion

class Agency(models.Model):
    agency_id = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    tz = models.CharField(max_length=25)
    
    def __unicode__(self):
        return self.name
    
class Source(models.Model):
    source_id = models.CharField(max_length=5)
    name = models.CharField(max_length=100)
    encoding = models.CharField(max_length=15, blank=True, default='utf-8')
    
    def __unicode__(self):
        return u"%s - %s" % (self.source_id, self.name)
    
class BaseStop(models.Model):
    common_name = models.CharField(max_length=100)
    common_city = models.CharField(max_length=50)
    stop_type = models.SmallIntegerField(choices=[(1,"Physical stop"), (2, "Logical stop")], default=1)    
    
    def __unicode__(self):
        return u"%s, %s" % (self.common_city, self.common_name)
    
    @staticmethod
    def search(terms):
        return BaseStop.objects.filter(models.Q(common_name__icontains=terms) | models.Q(common_city__icontains=terms)).filter(stop_type=2)

class UserStop(BaseStop, gis_models.Model):
    tpc = models.CharField(max_length=16, unique=True) #May change
    point = gis_models.PointField()
    objects = gis_models.GeoManager()
    
    ''' A physical stop denotes a physical location where a transport vehicle stops. A logical stop is composed of
    one or more physical stops (typically two, one for each direction'''
    parent = models.ForeignKey("BaseStop", blank=True, null=True, related_name="parent")

class StopAttribute(models.Model):
    stop = models.ForeignKey(BaseStop)
    key = models.CharField(max_length=20)
    value = models.CharField(max_length=256)
    
    class Meta:
        unique_together = (("stop", "key"),)
    
    def __unicode__(self):
        return u"%s: %s" % (self.stop, self.key)
    
class SourceAttribute(models.Model):
    stop = models.ForeignKey(BaseStop)
    source = models.ForeignKey(Source)
    key = models.CharField(max_length=20)
    value = models.CharField(max_length=256)

    class Meta:
        unique_together = (("stop", "key"),)    
    
    def __unicode__(self):
        return u"%s - %s: %s" % (self.source.name, self.stop, self.key)

class Route(models.Model):
    ''' Line / Lijnnummer (1, A, 4s, 122s, etc)'''
    common_code = models.CharField(max_length=5)
    ''' Destination / Eindbestemming (Station Arnhem, Velp Broekhuizerweg, Het Duifje)'''
    common_destination = models.CharField(max_length=100)
    
    
    origin = models.ForeignKey(BaseStop, related_name="origin")
    destination = models.ForeignKey(BaseStop, related_name="destination")
    
    ''' Collection of agencies that operate this route '''
    agencies=models.ManyToManyField(Agency)
    
    def __unicode__(self):
        return u"Lijn %s - %s" % (self.common_code, self.common_destination)

class Trip(models.Model):
    trip_id = models.CharField(max_length=10)
    route = models.ForeignKey(Route)

class TripSegment(gis_models.Model):
    trip = models.ForeignKey(Trip)
    
    ''' These names chosen because from is a protected keyword and start/end seems silly without _stop '''
    from_stop = models.ForeignKey(BaseStop, related_name="from_stop")
    to_stop = models.ForeignKey(BaseStop, related_name="to_stop")
    
    ''' Line of points between these two stops'''
    line = gis_models.LineStringField() 
    objects = gis_models.GeoManager()

    def __unicode__(self):
        return u"%s - %s" % (self.from_stop, self.to_stop)