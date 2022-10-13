from django.contrib import admin
from django.urls import path, include

from .api import assign_shifts, complete_shift, get_avail, get_shifts, post_avail, publish_shifts

urlpatterns=[
    path('shifts', get_shifts),
    path('assign-shifts', assign_shifts),
    path('publish-shifts', publish_shifts),
    path('complete-shift', complete_shift),
    path('get-avail', get_avail),
    path('post-avail', post_avail)
]