from django.contrib.gis import admin
from models import UserStop, BaseStop, Agency, Source, StopAttribute, SourceAttribute
import reversion

class StopAttributeInline(admin.TabularInline):
    model = StopAttribute
    
class SourceAttributeInline(admin.TabularInline):
    model = SourceAttribute

class StopAdmin(admin.OSMGeoAdmin, reversion.VersionAdmin):
    inlines = [
        StopAttributeInline,
        SourceAttributeInline
    ]

class AgencyAdmin(admin.ModelAdmin):
    model = Agency

class SourceAdmin(admin.ModelAdmin):
    model = Source
    
''' 
Please note, registering these models has the side-effect of registering them for
django-reversion and keeping track of revisions. Please think twice before removing 
'''
admin.site.register(BaseStop, StopAdmin)
admin.site.register(UserStop, StopAdmin)
admin.site.register(Agency, AgencyAdmin)
admin.site.register(Source, SourceAdmin)