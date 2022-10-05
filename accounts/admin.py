
from django.contrib import admin

from accounts.models import CarerProfile, HomeProfile, User

# Register your models here.
admin.site.register((User, HomeProfile, CarerProfile))