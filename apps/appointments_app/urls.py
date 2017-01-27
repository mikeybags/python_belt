from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^appointments$', index, name = 'home'),
    url(r'^add_appt$', add_appt, name = 'add_appt'),
    url(r'^appointments/(?P<id>\d+)$', edit_appt, name = 'edit_appt'),
    url(r'^appointments/(?P<id>\d+)/update$', update_appt, name = 'update_appt'),
    url(r'^appointments/destroy/(?P<id>\d+)$', remove_appt, name = 'remove_appt'),
]
