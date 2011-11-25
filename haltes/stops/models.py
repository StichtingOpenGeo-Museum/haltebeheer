from django.db import models
from django.contrib.gis.db import models 
from revisions import models as rev_models

class WorldBorder(models.Model):
    # Regular Django fields corresponding to the attributes in the
    # world borders shapefile.
    name = models.CharField(max_length=50)
    area = models.IntegerField()
    pop2005 = models.IntegerField('Population 2005')
    fips = models.CharField('FIPS Code', max_length=2)
    iso2 = models.CharField('2 Digit ISO', max_length=2)
    iso3 = models.CharField('3 Digit ISO', max_length=3)
    un = models.IntegerField('United Nations Code')
    region = models.IntegerField('Region Code')
    subregion = models.IntegerField('Sub-Region Code')
    lon = models.FloatField()
    lat = models.FloatField()

    # GeoDjango-specific: a geometry field (MultiPolygonField), and
    # overriding the default manager with a GeoManager instance.
    mpoly = models.MultiPolygonField()
    objects = models.GeoManager()

    # Returns the string representation of the model.
    def __unicode__(self):
        return self.name

class Agency(rev_models.TrashableModel):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=20)
    
class Stop(rev_models.TrashableModel):
    common_name = models.CharField(max_length=100)
    common_city = models.CharField(max_length=50)
    
    point = models.PointField()
    objects = models.GeoManager()
    
    def __unicode__(self):
        return "%s, %s" % (self.common_city, self.common_name)

class StopAttribute(rev_models.TrashableModel):
    stop = models.ForeignKey(Stop)
    key = models.CharField(max_length=20)
    value = models.CharField(max_length=256)
    
    def __unicode__(self):
        return "%s - %s" % (self.stop, self.key)
    
class AgencyAttribute(rev_models.TrashableModel):
    stop = models.ForeignKey(Stop)
    agency = models.ForeignKey(Agency)
    key = models.CharField(max_length=20)
    value = models.CharField(max_length=256)
    
    def __unicode__(self):
        return "%s - %s: %s" % (self.stop, self.stop, self.key)
    