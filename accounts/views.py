# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required,permission_required
from .forms import SignupForm, LoginForm
from django.http import HttpResponse
from .models import *

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # hash password
            user.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, "signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})



@login_required
def dashboard_view(request):
    if request.user.groups.filter(name='Teacher').exists():
        return HttpResponse("Welcome Teacher! You can add or change courses.")
    elif request.user.groups.filter(name='Student').exists():
        return HttpResponse("Welcome Student! You can only view courses.")
    else:
        return HttpResponse("Welcome! You have no special group assigned.")

def logout_view(request):
    logout(request)
    return redirect('login')

def course_create(request):
    if request.user.has_perm('authproject.add_course'):
        return HttpResponse("You can add a course!")
    else:
        return HttpResponse("You do not have permission to add courses.")


@permission_required('authproject.add_course')
def create_course(request):
    # Only teachers with add_course permission can access this
    return HttpResponse("Course added successfully!")

@permission_required('authproject.change_course')
def edit_course(request, course_id):
    # Only teachers with change_course permission can access this
    return HttpResponse("Course edited successfully!")

def course_list(request):
    # Everyone (students + teachers) can view courses
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})