from django.shortcuts import render

def index(request):
    return render(request, 'attendance/index.html')

def login_view(request):
    return render(request, 'attendance/login.html')
