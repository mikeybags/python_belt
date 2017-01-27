from django.shortcuts import render, redirect
from models import *
from django.contrib import messages

# Create your views here.
def index(request):
    if 'id' in request.session:
        request.session.clear()
    return render(request, 'login_app/index.html')

def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_pw = request.POST['confirm_pw']
        request.session['first_name'] = first_name
        request.session['last_name'] = last_name
        request.session['email'] = email
        errors = []
        errors += User.objects.validate(first_name, last_name, email, password, confirm_pw)
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            registration = User.objects.register(first_name, last_name, email, password)
            if 'errors' in registration:
                for error in registration['errors']:
                    messages.error(request, error)
            if 'user' in registration:
                request.session['id'] = registration['user'].id
                return redirect('/success')
    return redirect('/')

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
            request.session['first_name'] = login['user'].first_name
            return redirect('/success')
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def success(request):
    return render(request, 'login_app/success.html')
