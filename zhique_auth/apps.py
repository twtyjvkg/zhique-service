from django.apps import AppConfig


class ZhiqueAuthConfig(AppConfig):
    name = 'zhique_auth'

    def ready(self):
        from . import signals
