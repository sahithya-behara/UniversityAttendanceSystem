from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

# ✅ Custom User Model
class CustomUser(AbstractUser):
    USER_TYPES = (
        ('student', 'Student'),
        ('faculty', 'Faculty'),
    )

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, default="Unknown")
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='student')

    USERNAME_FIELD = 'email'  # ✅ Use email for login instead of username
    REQUIRED_FIELDS = ['full_name', 'user_type']  # ✅ Ensure user_type is required

    # Fix related_name conflicts with Django's default User model
    groups = models.ManyToManyField(
        'auth.Group',
        related_name="customuser_groups",
        blank=True
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name="customuser_permissions",
        blank=True
    )

    def __str__(self):
        return f"{self.full_name} ({self.get_user_type_display()})"


# ✅ Branch Model
class Branch(models.Model):
    name = models.CharField(max_length=100, unique=True)
    year_count = models.IntegerField(default=4, verbose_name="Number of Years")  # B.Tech = 4 years

    def __str__(self):
        return self.name


# ✅ Student Model
class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student')  # ❌ Fix orphaned users
    roll_number = models.CharField(max_length=20, unique=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, related_name='students')
    year = models.IntegerField(default=1, verbose_name="Year of Study")  # 1st, 2nd, 3rd, 4th year

    def __str__(self):
        return f"{self.user.full_name} - {self.roll_number}"


# ✅ Faculty Model
class Faculty(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='faculty')  # ❌ Fix orphaned users
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, related_name='faculties')
    designation = models.CharField(max_length=100, default='Not Assigned')  # Default designation
    is_class_teacher = models.BooleanField(default=False, verbose_name="Is Class Teacher")
    class_teacher_of_year = models.IntegerField(null=True, blank=True, verbose_name="Class Teacher of Year")  # Optional

    def clean(self):
        """Ensure 'class_teacher_of_year' is set only if 'is_class_teacher' is True"""
        if self.is_class_teacher and not self.class_teacher_of_year:
            raise ValidationError("Class teacher must specify a year!")
        if not self.is_class_teacher and self.class_teacher_of_year:
            self.class_teacher_of_year = None  # Auto-reset if not class teacher

    def __str__(self):
        return f"{self.user.full_name} - {self.designation}"


# ✅ Student Attendance Model
class StudentAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=20, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    class Meta:
        unique_together = ('student', 'date')  # ❌ Prevent duplicate attendance per day

    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"


# ✅ Faculty Attendance Model
class FacultyAttendance(models.Model):
    faculty = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    def __str__(self):
        return f"{self.faculty.name} - {self.date} - {self.status}"