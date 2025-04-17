from django.contrib import admin
from .models import Branch, Student, Faculty, StudentAttendance, FacultyAttendance

admin.site.register(Branch)
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(StudentAttendance)
admin.site.register(FacultyAttendance)
