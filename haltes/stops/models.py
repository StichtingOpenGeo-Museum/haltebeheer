from django.db import models
from django.contrib.gis.db import models 
import reversion

class Agency(models.Model):
    agency_id = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    tz = models.CharField(max_length=25)
    
    def __unicode__(self):
        return self.name
    
class Stop(models.Model):
    common_name = models.CharField(max_length=100)
    common_city = models.CharField(max_length=50)
    tpc = models.CharField(max_length=16) #May change
    
    stop_type = models.SmallIntegerField(choices=[(1,"Physical stop"), (2, "Logical stop")], default=1)
    ''' A physical stop denotes a physical location where a transport vehicle stops. A logical stop is composed of
    one or more physical stops (typically two, one for each direction'''
    parent = models.ForeignKey("Stop", blank=True, null=True)
    
    point = models.PointField()
    objects = models.GeoManager()
    
    def __unicode__(self):
        return u"%s, %s" % (self.common_city, self.common_name)
    
    @staticmethod
    def search(terms):
        return Stop.objects.filter(models.Q(common_name__icontains=terms) | models.Q(common_city__icontains=terms))
    
class StopAttribute(models.Model):
    stop = models.ForeignKey(Stop)
    key = models.CharField(max_length=20)
    value = models.CharField(max_length=256)
    
    class Meta:
        unique_together = (("stop", "key"),)
    
    def __unicode__(self):
        return u"%s: %s" % (self.stop, self.key)
    
class AgencyAttribute(models.Model):
    stop = models.ForeignKey(Stop)
    agency = models.ForeignKey(Agency)
    key = models.CharField(max_length=20)
    value = models.CharField(max_length=256)

    class Meta:
        unique_together = (("stop", "key"),)    
    
    def __unicode__(self):
        return u"%s - %s: %s" % (self.agency, self.stop, self.key)

class Route(models.Model):
    ''' Line / Lijnnummer (1, A, 4s, 122s, etc)'''
    common_code = models.CharField(max_length=5)
    ''' Destination / Eindbestemming (Station Arnhem, Velp Broekhuizerweg, Het Duifje)'''
    common_destination = models.CharField(max_length=100)
    
    
    origin = models.ForeignKey(Stop, related_name="origin")
    destination = models.ForeignKey(Stop, related_name="destination")
    
    ''' Collection of agencies that operate this route '''
    agencies=models.ManyToManyField(Agency)
    
    def __unicode__(self):
        return u"Lijn %s - %s" % (self.common_code, self.common_destination)

class RouteSegment(models.Model):
    route = models.ForeignKey(Route)
    
    ''' These names chosen because from is a protected keyword and start/end seems silly without _stop '''
    from_stop = models.ForeignKey(Stop, related_name="from_stop")
    to_stop = models.ForeignKey(Stop, related_name="to_stop")
    
    ''' Line of points between these two stops'''
    line = models.LineStringField() 
    objects = models.GeoManager()

    def __unicode__(self):
        return u"%s - %s" % (self.from_stop, self.to_stop)
