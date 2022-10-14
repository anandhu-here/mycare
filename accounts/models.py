from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, push_token=None, password=None, is_staff=False, is_active=True,  is_agent = False, is_admin=False, is_home = False, is_carer=False):
        if not email:
            raise ValueError('users must have a valid email')

        user_obj = self.model(
            email=email
        )
        user_obj.set_password(password)
        user_obj.push_token=push_token
        user_obj.staff = is_staff
        user_obj.home = is_home
        user_obj.carer = is_carer
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_carer_user(self, email, password, push_token):
        user= self.create_user(
            email,
            push_token=push_token,
            password=password,
            is_carer=True
        )
        return user


    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_staff=True,
            is_admin=True,
        )
        return user
    def create_home_user(self, email,push_token, password=None):
        user = self.create_user(
            email,
            push_token=push_token,
            password=password,
            is_home=True
        )
        return user

class User(AbstractBaseUser):
    email       = models.EmailField(blank=False, null=False, unique=True)
    standard    = models.CharField(max_length = 3, blank = True, null = True)
    push_token  = models.TextField(blank=True, null=True)
    score       = models.IntegerField(default = 16)
    first_login = models.BooleanField(default=False)
    active      = models.BooleanField(default=True)
    staff       = models.BooleanField(default=False)
    admin       = models.BooleanField(default=False)
    home        = models.BooleanField(default=False)
    carer       = models.BooleanField(default=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        if self.email:
            return str(self.email)
        else:return str(self.id)
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):

        return True

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active
    
    @property
    def is_home(self):
        return self.home

    @property
    def is_carer(self):
        return self.carer
    @property
    def is_staff(self):
        return self.staff


def imageUpload(self, filename):
    return f'images/profile/{self.user.email}/{filename}'
def fileUPload(self, filename):
    return f'files/{self.profile.first_name} - {self.profile.id}/{filename}'   


class CarerProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    dob = models.CharField(max_length=10,blank=True, null=True )
    phone = models.CharField(max_length = 13 , blank=True, null=True)
    dp = models.ImageField(imageUpload, blank=True, null = True)
    timestamp = models.DateField(auto_now_add=True)
    def __str__(self):
        if self.first_name:
            return self.first_name
        else:
            return str(self.id)



class HomeProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    street = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=13 ,blank=True, null=True)
    postcode = models.CharField(max_length=9, blank=True, null=True)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name 




def user_did_save(sender, instance, created, *args, **kwargs):
    if created:
        if instance.is_home:
            HomeProfile.objects.get_or_create(user=instance)
        if instance.is_carer:
            CarerProfile.objects.get_or_create(user=instance)

post_save.connect(user_did_save, sender=User)


