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


    def validate_appt(self, date, time):
        errors = []
        print time, "is time"
        if date < datetime.date.today().isoformat():
            errors.append("Appointments cannot be for the past!")
        if date == datetime.date.today().isoformat():
            if time < datetime.datetime.now().time().isoformat():
                errors.append("Appointments cannot be for the past!")
        appointments = Appointment.objects.filter(date = date)
        for appt in appointments:
            if time == appt.time:
                errors.append
        return errors




class Appointment(models.Model):
    task = models.CharField(max_length=50)
    status = models.CharField(max_length=10, default="Pending")
    time = models.TimeField()
    date = models.DateField()
    user = models.ForeignKey(User, related_name = "user_appointment")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AppointmentManager()
