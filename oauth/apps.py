from django.apps import AppConfig


class OAuthConfig(AppConfig):
    name = 'oauth'

    def ready(self):
        from . import signals
