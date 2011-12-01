from django.contrib.gis import admin
from models import Stop, Agency, StopAttribute, AgencyAttribute
import reversion

class StopAttributeInline(admin.TabularInline):
    model = StopAttribute
    
class AgencyAttributeInline(admin.TabularInline):
    model = AgencyAttribute

class StopAdmin(admin.OSMGeoAdmin, reversion.VersionAdmin):
    inlines = [
        StopAttributeInline,
        AgencyAttributeInline
    ]

class AgencyAdmin(reversion.VersionAdmin):
    model = AgencyAttribute
    
admin.site.register(Stop, StopAdmin)
admin.site.register(Agency, AgencyAdmin)
