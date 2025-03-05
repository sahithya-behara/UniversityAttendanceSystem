from django.contrib import admin
from .models import ClassManagement, Attendance  # Removed Dashboard

admin.site.register(ClassManagement)
admin.site.register(Attendance)
