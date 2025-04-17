from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Student, Faculty, StudentAttendance, FacultyAttendance, Branch
from .forms import StudentRegistrationForm, FacultyRegistrationForm, LoginForm

# Index Page
def index(request):
    return render(request, "attendance/index.html")

# Register Page
def register(request):
    return render(request, "attendance/register.html")

# Student Registration
def student_register(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"].strip().lower()
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Email already registered. Try logging in.")
                return redirect("login")
            try:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data["password1"])
                user.user_type = "student"
                user.username = email
                user.save()
                Student.objects.create(
                    user=user,
                    roll_number=form.cleaned_data["roll_number"],
                    branch=form.cleaned_data["branch"],
                    year=form.cleaned_data["year"]
                )
                messages.success(request, "Student registered successfully! Please log in.")
                return redirect("login")
            except Exception as e:
                messages.error(request, f"Error occurred: {str(e)}")
                return redirect("student_register")
    else:
        form = StudentRegistrationForm()
    branches = Branch.objects.all()
    return render(request, "attendance/student_register.html", {"form": form, "branches": branches})

# Faculty Registration
def faculty_register(request):
    if request.method == "POST":
        form = FacultyRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"].strip().lower()
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Email already registered. Try logging in.")
                return redirect("login")
            try:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data["password1"])
                user.user_type = "faculty"
                user.username = email
                user.save()
                Faculty.objects.create(
                    user=user,
                    designation=form.cleaned_data["designation"],
                    branch=form.cleaned_data["branch"],
                    is_class_teacher=form.cleaned_data["is_class_teacher"]
                )
                messages.success(request, "Faculty registered successfully! Please log in.")
                return redirect("login")
            except Exception as e:
                messages.error(request, f"Error occurred: {str(e)}")
                return redirect("faculty_register")
    else:
        form = FacultyRegistrationForm()
    branches = Branch.objects.all()
    return render(request, "attendance/faculty_register.html", {"form": form, "branches": branches})

# User Login
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"].strip().lower()
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome, {user.full_name}!")
                return redirect("home")
            else:
                messages.error(request, "Invalid email or password. Please try again.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = LoginForm()
    return render(request, "attendance/login.html", {"form": form})

# User Logout
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")

# Home Page (After Login)
# Home Page (After Login)
@login_required
def home(request):
    user = request.user
    user_details = {
        "name": user.full_name,
        "email": user.email,
        "role": "Student" if user.user_type == "student" else "Faculty"
    }

    # For Student users
    if user.user_type == 'student':
        user_details.update({
            "roll_number": user.student.roll_number,
            "branch": user.student.branch.name if user.student.branch else "Not Assigned",
            "year": user.student.year
        })
    
    # For Faculty users
    elif user.user_type == 'faculty':
        user_details.update({
            "designation": user.faculty.designation,
            "branch": user.faculty.branch.name if user.faculty.branch else "Not Assigned",
            "is_class_teacher": "Yes" if user.faculty.is_class_teacher else "No",
            # Add a link to the Faculty Attendance page for faculty users
            "faculty_attendance_link": "faculty_attendance"
        })

    return render(request, "attendance/home.html", {"user_details": user_details})


# Student Attendance Page
@login_required
def student_attendance(request):
    if request.user.user_type not in ['student', 'faculty']:
        messages.error(request, "You are not authorized to view this page.")
        return redirect("home")

    if request.user.user_type == 'student':
        attendance_records = StudentAttendance.objects.filter(student=request.user.student).select_related('student')
    else:
        attendance_records = StudentAttendance.objects.all()

    return render(request, "attendance/student_attendance.html", {"attendance_records": attendance_records})

# Add Student Page
@login_required
def add_student(request):
    if request.user.user_type != 'faculty':  
        messages.error(request, "Only faculty can access this page.")
        return redirect("home")

    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        roll_number = request.POST["roll_number"]
        branch = request.POST["branch"]
        year = request.POST["year"]
        password = request.POST["password"]

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists. Try another.")
            return redirect("add_student")
        if CustomUser.objects.filter(roll_number=roll_number).exists():
            messages.error(request, "Roll Number already exists.")
            return redirect("add_student")

        student = CustomUser.objects.create(
            username=email,
            email=email,
            full_name=name,
            roll_number=roll_number,
            branch=branch,
            year=year,
            user_type="student",  
            password=make_password(password)  
        )

        messages.success(request, "Student added successfully! They can now log in.")
        return redirect("home")  

    return render(request, "attendance/add_student.html")

# Mark Attendance Page
@login_required
def mark_attendance(request):
    if request.user.user_type != 'faculty':
        messages.error(request, "Only faculty can mark attendance.")
        return redirect("home")

User = get_user_model()
@login_required
def faculty_attendance(request):
    today = timezone.now().date()

    # Get the faculty instance for the currently logged-in user
    try:
        faculty_user = Faculty.objects.get(user=request.user)
    except Faculty.DoesNotExist:
        return HttpResponse("You are not registered as faculty.")

    # Get all faculty members from the same branch as the logged-in faculty
    faculty_qs = Faculty.objects.filter(branch=faculty_user.branch)

    faculty_data = []

    # Build data list with current attendance status
    for faculty in faculty_qs:
        attendance = FacultyAttendance.objects.filter(faculty=faculty, date=today).first()
        faculty_data.append({
            'id': faculty.id,
            'name': faculty.user.full_name,  # Accessing full name from CustomUser
            'status': attendance.status if attendance else '',
        })

    if request.method == "POST":
        for faculty in faculty_data:
            status = request.POST.get(f'attendance_{faculty["id"]}')
            if status:
                FacultyAttendance.objects.update_or_create(
                    faculty_id=faculty["id"],
                    date=today,
                    defaults={'status': status}
                )
        return render(request, "attendance/faculty_attendance.html", {
            'faculty_members': faculty_data,
            'attendance_marked': True,
            'today': today
        })

    return render(request, "attendance/faculty_attendance.html", {
        'faculty_members': faculty_data,
        'today': today
    })
def leave_management(request):
    # You can add any logic or context here if needed
    return render(request, 'attendance/leave_management.html')
