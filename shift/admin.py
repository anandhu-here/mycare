from django.contrib import admin

from shift.models import Availability, Shift

# Register your models here.

admin.site.register((Shift, Availability)   )