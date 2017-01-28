from django.shortcuts import render, redirect
import datetime
from .models import *
from django.contrib import messages


def index(request):
    if 'id' not in request.session:
        return redirect('login:index')
    user_id = request.session['id']
    today = datetime.date.today()
    today_iso = datetime.date.today().isoformat()
    appointments_today = Appointment.objects.filter(user = user_id).filter(date = today_iso).order_by('time')
    other_appointments = Appointment.objects.filter(user = user_id).exclude(date = today_iso).order_by('date', 'time')
    context = {'today': today,
               'appointments_today': appointments_today,
               'other_appointments': other_appointments
               }
    return render(request, 'appointments_app/home.html', context)


def add_appt(request):
    if request.method == 'POST':
        date = request.POST['date']
        date = date.encode('ascii','ignore')
        time = request.POST['time']
        time = time.encode('ascii','ignore')
        task = request.POST['task']
        user_id = request.session['id']
        errors = []
        errors += Appointment.objects.validate_appt(date, time)
        if errors:
            for error in errors:
                messages.error(request, error)
                return redirect('appointments:home')
        appointments = Appointment.objects.filter(date = date)
        for appt in appointments:
            if time == appt.time:
                error += "You cannot schedule two appointments at the same time!"
                messages.error(request, error)
                return redirect('appointments:home')
        Appointment.objects.add_appointment(task, date, time, user_id)
        return redirect('appointments:home')

    return redirect('appointments:home')

def edit_appt(request, id):
    if 'id' not in request.session:
        return redirect('login:index')
    appointment = Appointment.objects.get(id = id)
    context = {'appointment': appointment}
    return render(request, 'appointments_app/edit.html', context)

def update_appt(request, id):
    if 'id' not in request.session:
        return redirect('login:index')
    if request.method == 'POST':
        date = request.POST['date']
        date = date.encode('ascii','ignore')
        time = request.POST['time']
        time = time.encode('ascii','ignore')
        task = request.POST['task']
        status = request.POST['status']
        user_id = request.session['id']
        errors = []
        errors += Appointment.objects.validate_appt(date, time)
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            Appointment.objects.filter(id = id).update(date = date, time = time, status = status, task= task)
    return redirect('appointments:home')

def remove_appt(request, id):
        if 'id' not in request.session:
            return redirect('login:index')
        Appointment.objects.filter(id=id).delete()
        return redirect('appointments:home')
