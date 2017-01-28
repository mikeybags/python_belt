from django.shortcuts import render, redirect
import datetime
from .models import *
from django.contrib import messages


def index(request):
    if 'id' not in request.session:
        return redirect('login:index')
    user_id = request.session['id']
    today = datetime.date.today()
    current_time = datetime.datetime.now().time()
    print current_time
    today_iso = datetime.date.today().isoformat()
    appointments_today = Appointment.objects.filter(user = user_id).filter(date = today_iso).exclude(time__lt= current_time).order_by('time')
    for a in appointments_today:
        print a.time
    other_appointments = Appointment.objects.filter(user = user_id).exclude(date__lte= today_iso).order_by('date', 'time')
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
        errors += Appointment.objects.validate_appt(user_id, date, time)
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
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
        errors = []
        if request.POST['date']:
            date = request.POST['date']
            date = date.encode('ascii','ignore')
            errors += Appointment.objects.validate_appt(user_id, date)
            Appointment.objects.filter(id = id).update(date = date)
        if request.POST['time']:
            time = request.POST['time']
            time = time.encode('ascii','ignore')
            errors += Appointment.objects.validate_appt(user_id, None, time)
            Appointment.objects.filter(id = id).update(time = time)
        task = request.POST['task']
        status = request.POST['status']
        user_id = request.session['id']
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            Appointment.objects.filter(id = id).update(status = status, task= task)
    return redirect('appointments:home')

def remove_appt(request, id):
        Appointment.objects.filter(id=id).delete()
        return redirect('appointments:home')
