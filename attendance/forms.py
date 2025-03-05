from django import forms
from .models import Student  # Importing Student model if it exists

class AttendanceForm(forms.Form):
    # Class Choices (Modify this if class data comes from DB)
    class_choices = [
        ('class1', 'Class 1'),
        ('class2', 'Class 2'),
        ('class3', 'Class 3'),
    ]
    class_name = forms.ChoiceField(choices=class_choices, label='Select Class')

    # Dynamically generate checkboxes for students
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        students = Student.objects.all()  # Fetch students from the database
        for student in students:
            self.fields[f'student_{student.id}'] = forms.BooleanField(
                required=False,
                label=student.name  # Assuming the Student model has a `name` field
            )
