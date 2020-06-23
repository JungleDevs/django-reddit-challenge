"""
S3 helper
"""
###
# Libraries
###
import os

from django.utils.deconstruct import deconstructible
from django.utils import timezone


###
# Upload images to S3 storage
###
@deconstructible
class UploadFileTo(object):
    def __init__(self, folder, suffix):
        self.folder = folder
        self.suffix = suffix

    def __call__(self, instance, filename):
        filename_base, filename_ext = os.path.splitext(filename)
        return '{0}/{1}{2}'.format(
            self.folder,
            '{0}-{1}-{2}'.format(instance.uuid, self.suffix, timezone.now().isoformat()),
            filename_ext.lower(),
        )
