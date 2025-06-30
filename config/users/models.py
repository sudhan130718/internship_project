from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

     # Address Fields
    address1 = models.CharField("Address Line 1", max_length=255, default="Not provided")
    address2 = models.CharField("Address Line 2", max_length=255, blank=True, default="")
    city = models.CharField(max_length=100, default="Unknown")
    state = models.CharField(max_length=100, default="Unknown")
    pincode = models.CharField(max_length=10, default="000000")

    def __str__(self):
        return self.user.username