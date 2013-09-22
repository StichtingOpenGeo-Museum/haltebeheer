from haltes.stops.models import BaseStop
from haltes.batch.models import Error
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

class BaseStopInline(admin.TabularInline):
    model = Error.affects.through
    
class ErrorAdmin(ModelAdmin):
    inlines = [ BaseStopInline ]
    # TODO Hide Affects
    #fields = 

admin.site.register(Error, ErrorAdmin)