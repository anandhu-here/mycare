from django.db import models
from accounts.models import HomeProfile, CarerProfile
# Create your models here.


class Shift(models.Model):
    home = models.ForeignKey(HomeProfile, on_delete=models.CASCADE, blank=True, null=True)
    day = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()
    assigned = models.ManyToManyField(CarerProfile, blank=True, null=True, related_name="assigned_user")
    covered = models.ManyToManyField(CarerProfile,  blank=True, null=True)
    def __str__(self):
        return str(self.day) + "/" + str(self.month) + "/" + str(self.year) + ":" + str(self.home.name)



class Availability(models.Model):
    mon = models.BooleanField(default=False)
    tue = models.BooleanField(default=False)
    web = models.BooleanField(default=False)
    thu = models.BooleanField(default=False)
    fri = models.BooleanField(default=False)
    sat = models.BooleanField(default=False)
    sun = models.BooleanField(default=False)
    carer = models.ForeignKey(CarerProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.carer.first_name