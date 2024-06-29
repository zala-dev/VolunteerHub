from django.contrib import admin
from .models import VolunteeringEvent, Like, Donation

admin.site.register(VolunteeringEvent)
admin.site.register(Like)
admin.site.register(Donation)