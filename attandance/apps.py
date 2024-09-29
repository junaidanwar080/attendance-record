from django.apps import AppConfig

class AttendanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'attandance'

    # def ready(self):
    #     import attandance.signals  # Import the signals module to register signal handlers
