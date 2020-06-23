"""
Accounts Models
"""
###
# Libraries
###
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext as _


###
# Choices
###


###
# Querysets
###


###
# Models
###
class User(AbstractUser):
    # Override user model here
    pass


class ChangeEmailRequest(models.Model):
    # Helpers
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        verbose_name=_('uuid'),
    )

    # User model
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='change_email_request',
        verbose_name=_('user'),
    )

    # Email
    email = models.EmailField(verbose_name=_('email'))
