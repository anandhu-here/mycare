from email.policy import default
from django.db import models
from accounts.models import HomeProfile, CarerProfile
# Create your models here.


class Shift(models.Model):
    home = models.ForeignKey(HomeProfile, on_delete=models.CASCADE, blank=True, null=True)
    day = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()
    longday = models.IntegerField()
    night = models.IntegerField()
    late = models.IntegerField()
    early = models.IntegerField()
    def __str__(self):
        return str(self.day) + "/" + str(self.month) + "/" + str(self.year) + ":" + str(self.home.name)

class AssignedCarer(models.Model):
    carer = models.ForeignKey(CarerProfile, on_delete=models.CASCADE)
    type = models.CharField(choices=(('LONGDAY', 'LONGDAY'), ('NIGHT', 'NIGHT'), ('EARLY', 'EARLY'), ('LATE', 'LATE')), max_length=100)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    covered = models.BooleanField(default=False)
    def __str__(self):
        return str(self.carer.first_name)

class Availability(models.Model):
    mon = models.BooleanField(default=False)
    tue = models.BooleanField(default=False)
    wed = models.BooleanField(default=False)
    thu = models.BooleanField(default=False)
    fri = models.BooleanField(default=False)
    sat = models.BooleanField(default=False)
    sun = models.BooleanField(default=False)
    carer = models.ForeignKey(CarerProfile, on_delete=models.CASCADE)
    count = models.IntegerField()
    def __str__(self):
        return self.carer.first_name