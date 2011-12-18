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
    tpc = models.CharField(max_length=16)
    
    point = models.PointField()
    objects = models.GeoManager()
    
    def __unicode__(self):
        return u"%s, %s" % (self.common_city, self.common_name)
    
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

#reversion.register(Stop, follow=["stopattribute_set", "agencyattribute_set"])
#reversion.register(StopAttribute)    
#reversion.register(AgencyAttribute)