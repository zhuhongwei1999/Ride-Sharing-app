from django.apps import AppConfig


class RidesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rides'
    
    def ready(self):
        import users.signals