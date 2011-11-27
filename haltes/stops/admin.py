from django.contrib.gis import admin
from models import Stop, Agency, StopAttribute, AgencyAttribute

class StopAttributeInline(admin.TabularInline):
    model = StopAttribute
    
class AgencyAttributeInline(admin.TabularInline):
    model = AgencyAttribute

class StopAdmin(admin.OSMGeoAdmin):
    inlines = [
        StopAttributeInline,
        AgencyAttributeInline
    ]

class AgencyAdmin(admin.ModelAdmin):
    model = AgencyAttribute
    
admin.site.register(Stop, StopAdmin)
admin.site.register(Agency, AgencyAdmin)
