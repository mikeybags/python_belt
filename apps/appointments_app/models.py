from __future__ import unicode_literals
import datetime
from django.db import models
from ..login_app.models import User

# Create your models here.
class AppointmentManager(models.Manager):
    def add_appointment(self, task, date, time, user_id):
        user = User.objects.get(id = user_id)
        Appointment.objects.create(task = task, date = date, time = time, user = user)
        return True

    def validate_appt(self, user_id, date = None, time = None, id = None):
        errors = []
        print time, "is time 1"
        print date, "is date 2"
        if date < datetime.date.today().isoformat():
            errors.append("Appointments cannot be for the past!")
        if date == datetime.date.today().isoformat():
            if time < datetime.datetime.now().time().isoformat():
                errors.append("Appointments cannot be for the past!")
        if Appointment.objects.filter(user__id = user_id).filter(date = date).filter(time = time).exclude(id = id):
            errors.append('You can not schedule two appointments at the same time.')
        return errors

class Appointment(models.Model):
    task = models.CharField(max_length=50)
    status = models.CharField(max_length=10, default="pending")
    time = models.TimeField()
    date = models.DateField()
    user = models.ForeignKey(User, related_name = "user_appointment")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AppointmentManager()
