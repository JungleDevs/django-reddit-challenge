"""
Model helper
"""
###
# Libraries
###
from django.db import models


###
# Helpers
###
class TimestampModel(models.Model):
    '''
        Extend this model if you wish to have automatically updated
        created_at and updated_at fields.
    '''

    class Meta:
        abstract = True

    created_at = models.DateTimeField(null=False, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=False, blank=True, auto_now=True)
