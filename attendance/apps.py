from django.apps import AppConfig

class AttendanceConfig(AppConfig):
    # This specifies the default field type for auto-incrementing primary keys in models.
    default_auto_field = 'django.db.models.BigAutoField'
    
    # The name of the Django app, which is used to reference the app in your project.
    name = 'attendance'
