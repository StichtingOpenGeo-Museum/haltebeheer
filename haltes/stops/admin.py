from django.contrib.gis import admin
from models import BaseStop, Agency, Source, StopAttribute, SourceAttribute
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

class AgencyAdmin(reversion.VersionAdmin):
    model = Agency

class SourceAdmin(reversion.VersionAdmin):
    model = Source
    
admin.site.register(BaseStop, StopAdmin)
admin.site.register(Agency, AgencyAdmin)
admin.site.register(Source, SourceAdmin)