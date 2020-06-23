"""
Accounts admin
"""
###
# Libraries
###
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from . import models


###
# Inline Admin Models
###


###
# Main Admin Models
###
@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'email', 'username', 'is_active', 'last_login', 'date_joined',)

@admin.register(models.ChangeEmailRequest)
class ChangeEmailRequestAdmin(admin.ModelAdmin):
    list_display = ('email',)
    readonly_fields = ('uuid',)
