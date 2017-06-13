from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^$', index, name = 'home'),
    url(r'^add_appt$', add_appt, name = 'add_appt'),
    url(r'^(?P<id>\d+)/edit$', edit_appt, name = 'edit_appt'),
    url(r'^(?P<id>\d+)/update$', update_appt, name = 'update_appt'),
    url(r'^(?P<id>\d+)/destroy$', remove_appt, name = 'remove_appt'),
]
