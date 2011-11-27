from django.db import models
from django.contrib.gis.db import models 
from revisions import models as rev_models, shortcuts

class Agency(rev_models.TrashableModel, rev_models.VersionedModel, shortcuts.VersionedModel):
    agency_id = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    tz = models.CharField(max_length=25)
    
class Stop(rev_models.TrashableModel, rev_models.VersionedModel, shortcuts.VersionedModel):
    common_name = models.CharField(max_length=100)
    common_city = models.CharField(max_length=50)
    
    point = models.PointField()
    objects = models.GeoManager()
    
    def __unicode__(self):
        return "%s, %s" % (self.common_city, self.common_name)

class StopAttribute(rev_models.TrashableModel, rev_models.VersionedModel, shortcuts.VersionedModel):
    stop = models.ForeignKey(Stop)
    key = models.CharField(max_length=20)
    value = models.CharField(max_length=256)
    
    def __unicode__(self):
        return "%s - %s" % (self.stop, self.key)
    
class AgencyAttribute(rev_models.TrashableModel, rev_models.VersionedModel, shortcuts.VersionedModel):
    stop = models.ForeignKey(Stop)
    agency = models.ForeignKey(Agency)
    key = models.CharField(max_length=20)
    value = models.CharField(max_length=256)
    
    def __unicode__(self):
        return "%s - %s: %s" % (self.stop, self.stop, self.key)
    