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
    list_display = ('__unicode__', 'stop_type')
    list_filter = ('stop_type',)
    search_fields = ['common_name','common_city']
    
class UserStopAdmin(StopAdmin):
    list_filter = ()
    list_display = ('__unicode__', 'has_parent')
    actions = ['merge_stops']
    
    def has_parent(self, obj):
      return (obj.parent is not None)
    has_parent.short_description = "Has parent?"
    
    def merge_stops(self, request, queryset):
        base_stop = BaseStop(common_name=queryset[0].common_name, common_city=queryset[1].common_name)
        base_stop.save()
        for obj in queryset:
            obj.parent = base_stop
            obj.save()
        self.message_user(request, "%s added as logical parent stop" % base_stop)
    merge_stops.short_description = "Add stops to same logical stop"

class AgencyAdmin(admin.ModelAdmin):
    model = Agency

class SourceAdmin(admin.ModelAdmin):
    model = Source
    
''' 
Please note, registering these models has the side-effect of registering them for
django-reversion and keeping track of revisions. Please think twice before removing 
'''
admin.site.register(BaseStop, StopAdmin)
admin.site.register(UserStop, UserStopAdmin)
admin.site.register(Agency, AgencyAdmin)
admin.site.register(Source, SourceAdmin)