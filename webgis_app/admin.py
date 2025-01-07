from django.contrib.gis import admin
from .models import MyLocation, Hospital

@admin.register(Hospital)
class HospitalAdmin(admin.GISModelAdmin):
    list_display = ('name', 'type', 'location')

@admin.register(MyLocation)
class UserLocationAdmin(admin.GISModelAdmin):
    list_display = ('name', 'location', 'description')
