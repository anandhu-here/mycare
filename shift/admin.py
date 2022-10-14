from django.contrib import admin

from shift.models import AssignedCarer, Availability, Shift

# Register your models here.

admin.site.register((Shift, Availability, AssignedCarer)   )