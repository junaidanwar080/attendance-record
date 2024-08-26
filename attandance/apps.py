from django.apps import AppConfig

class AttendanceConfig(AppConfig):
    name = 'attandance'

    def ready(self):
        import attandance.signals  # Import the signals module to register signal handlers
