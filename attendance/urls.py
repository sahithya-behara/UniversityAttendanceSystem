from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),  # ✅ Index Page
    path("register/", views.register, name="register"),  # ✅ Registration Selection Page
    path("register/student/", views.student_register, name="student_register"),  # ✅ Student Registration
    path("register/faculty/", views.faculty_register, name="faculty_register"),  # ✅ Faculty Registration
    path("login/", views.login_view, name="login"),  # ✅ User Login
    path("logout/", views.user_logout, name="logout"),  # ✅ User Logout
    path("home/", views.home, name="home"),  # ✅ Home Page (After Login)
    path("attendance/student/", views.student_attendance, name="student_attendance"),  # ✅ Student Attendance Page
    path("attendance/faculty/", views.faculty_attendance, name="faculty_attendance"),  # ✅ Faculty Attendance Page
    path("add_student/", views.add_student, name="add_student"),  # ✅ Add Student Page
    path("attendance/mark_attendance/", views.mark_attendance, name="mark_attendance"),  # ✅ Mark Attendance Page
    path("attendance/faculty_attendance/", views.faculty_attendance, name="faculty_attendance"),
     path('leave-management/', views.leave_management, name='leave_management'), 
]
