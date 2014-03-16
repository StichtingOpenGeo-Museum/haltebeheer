from django.db import models
from stops.models import BaseStop

class Error(models.Model):
    ''' Store errors that we come across with several algorithms on stops'''
    
    # Which stops does this affect? (What, Where)
    affects = models.ManyToManyField(BaseStop, related_name="affects")
    
    # Describe the error (Why, How, Where)    
    # Every error must have one of these three error levels
    ERROR_LEVELS = ((1, 'Error'),
                    (2, 'Warning'),
                    (3, 'Info'))
    severity = models.CharField(max_length=1, choices=ERROR_LEVELS, blank=False)
    code = models.CharField(max_length=5)
    message = models.CharField(max_length=255)
    
    # (When)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)