from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import Student, Faculty, StudentAttendance, FacultyAttendance, Branch

CustomUser = get_user_model()  # Get the CustomUser model

# ✅ Student Registration Form
class StudentRegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder': 'Full Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    roll_number = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'placeholder': 'Roll Number'}))
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), empty_label="Select Branch", required=True)
    year = forms.IntegerField(min_value=1, max_value=4, required=True, widget=forms.NumberInput(attrs={'placeholder': 'Year'}))

    class Meta:
        model = CustomUser
        fields = ["full_name", "email", "roll_number", "year", "branch", "password1", "password2"]

    def clean_email(self):
        """Ensure email is unique in CustomUser model."""
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Email already exists!")
        return email

    def save(self, commit=True):
        """Save student and link to user."""
        user = super().save(commit=False)
        user.user_type = "student"
        user.set_password(self.cleaned_data["password1"])  # Ensure password is hashed
        if commit:
            user.save()
            Student.objects.create(
                user=user,
                roll_number=self.cleaned_data["roll_number"],
                branch=self.cleaned_data["branch"],
                year=self.cleaned_data["year"]
            )
        return user

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Branch, Faculty

# ✅ Faculty Registration Form
class FacultyRegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder': 'Full Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    designation = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Designation'}))
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), empty_label="Select Branch", required=True)
    is_class_teacher = forms.BooleanField(required=False)

    class Meta:
        model = CustomUser
        fields = ["full_name", "email", "designation", "branch", "is_class_teacher", "password1", "password2"]

    def clean_email(self):
        """Ensure email is unique in CustomUser model."""
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Email already exists!")
        return email

    def save(self, commit=True):
        """Save faculty and link to user."""
        user = super().save(commit=False)
        user.user_type = "faculty"
        user.set_password(self.cleaned_data["password1"])  # Ensure password is hashed
        if commit:
            user.save()
            Faculty.objects.create(
                user=user,
                designation=self.cleaned_data["designation"],
                branch=self.cleaned_data["branch"],
                is_class_teacher=self.cleaned_data["is_class_teacher"]
            )
        return user


    def save(self, commit=True):
        """Save faculty user and faculty profile."""
        user = super().save(commit=False)
        user.full_name = self.cleaned_data["full_name"]  
        user.user_type = "faculty"
        user.username = self.cleaned_data["email"]  # ✅ Set username as email to avoid UNIQUE constraint issue
        user.set_password(self.cleaned_data["password1"])  

        if commit:
            user.save()
            Faculty.objects.create(
                user=user,
                branch=self.cleaned_data["branch"],
                designation=self.cleaned_data["designation"],
                is_class_teacher=self.cleaned_data["is_class_teacher"]
            )
        return user


# ✅ Student Attendance Form
class StudentAttendanceForm(forms.ModelForm):
    class Meta:
        model = StudentAttendance
        fields = ["student", "date", "status"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "status": forms.Select(choices=[("Present", "Present"), ("Absent", "Absent")])
        }

# ✅ Faculty Attendance Form
class FacultyAttendanceForm(forms.ModelForm):
    class Meta:
        model = FacultyAttendance
        fields = ["faculty", "date", "status"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "status": forms.Select(choices=[("Present", "Present"), ("Absent", "Absent")])
        }

# ✅ Login Form
from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"}),
        required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=True
    )
