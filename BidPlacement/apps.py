from django.apps import AppConfig

class BidPlacementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'BidPlacement'

    def ready(self):
        import BidPlacement.signals
