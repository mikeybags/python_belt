from django.shortcuts import render, redirect
from models import *
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'login_app/index.html')

def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_pw = request.POST['confirm_pw']
        date_of_birth = request.POST['date_of_birth']
        date_of_birth = date_of_birth.encode('ascii','ignore')
        request.session['first_name'] = first_name
        request.session['last_name'] = last_name
        request.session['email'] = email
        errors = []
        errors += User.objects.validate(first_name, last_name, email, password, confirm_pw, date_of_birth)
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            registration = User.objects.register(first_name, last_name, email, password, date_of_birth)
            if 'errors' in registration:
                for error in registration['errors']:
                    messages.error(request, error)
            if 'user' in registration:
                request.session['id'] = registration['user'].id
                return redirect('appointments:home')
    return redirect('login:index')

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        request.session['login_email'] = email
        password = request.POST['password']
        login = User.objects.authenticate(email, password)
        if 'errors' in login:
            for error in login['errors']:
                messages.error(request, error)
        else:
            request.session['id'] = login['user'].id
            request.session['first_name'] = login['user'].first_name
            return redirect('appointments:home')
    return redirect('login:index')

def logout(request):
    request.session.clear()
    return redirect('login:index')
