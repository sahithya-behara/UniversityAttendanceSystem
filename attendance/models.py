from django.db import models

class ClassManagement(models.Model):
    class_name = models.CharField(max_length=100)
    section = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.class_name} - {self.section}"

class Attendance(models.Model):
    student_name = models.CharField(max_length=100)
    class_attended = models.ForeignKey(ClassManagement, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    def __str__(self):
        return f"{self.student_name} - {self.status} ({self.date})"
