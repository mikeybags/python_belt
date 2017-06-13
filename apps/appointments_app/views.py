from django.shortcuts import render, redirect
import datetime
from .models import *
from django.contrib import messages


def index(request):
    if 'id' not in request.session:
        return redirect('login:index')
    user_id = request.session['id']
    today = datetime.datetime.now().date()
    current_time = datetime.datetime.now().time()
    appointments_today = Appointment.objects.filter(user = user_id).filter(date = today).exclude(time__lt= current_time).order_by('time')
    other_appointments = []
    for a in appointments_today:
        other_appointments = Appointment.objects.filter(user = user_id).exclude(date__lte= today).order_by('date', 'time')
    context = {'today': today,
               'appointments_today': appointments_today,
               'other_appointments': other_appointments
               }
    return render(request, 'appointments_app/home.html', context)

def add_appt(request):
    if request.method == 'POST':
        date = request.POST['date']
        time = request.POST['time']
        task = request.POST['task']
        user_id = request.session['id']
        errors = []
        errors += Appointment.objects.validate_appt(user_id, date, time)
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            Appointment.objects.add_appointment(task, date, time, user_id)
    return redirect('appointments:home')

def edit_appt(request, id):
    if 'id' not in request.session:
        return redirect('login:index')
    appointment = Appointment.objects.get(id = id)
    appointment_time = str(appointment.time)
    appointment_date = str(appointment.date)
    context = {
        'appointment': appointment,
        'appointment_date': appointment_date,
        'appointment_time': appointment_time
        }
    return render(request, 'appointments_app/edit.html', context)

def update_appt(request, id):
    if 'id' not in request.session:
        return redirect('login:index')
    user_id = request.session['id']
    if request.method == 'POST':
        errors = []
        task = request.POST['task']
        status = request.POST['status']
        user_id = request.session['id']
        time = request.POST['time']
        date = request.POST['date']
        errors += Appointment.objects.validate_appt(user_id, date, time, id)
        if errors:
            for error in errors:
                messages.error(request, error)
                return redirect('appointments:edit_appt', id = id)
        else:
            Appointment.objects.filter(id = id).update(status = status, task= task, time = time, date = date)
    return redirect('appointments:home')

def remove_appt(request, id):
        Appointment.objects.filter(id=id).delete()
        return redirect('appointments:home')
