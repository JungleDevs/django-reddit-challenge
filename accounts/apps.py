"""
Accounts Apps
"""
###
# Libraries
###
from django.apps import AppConfig


###
# Config
###
class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        import accounts.signals
