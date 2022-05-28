from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class ExtendUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=300)
    phone = models.CharField(max_length=16)
    picture = models.ImageField(upload_to='images')

    def __str__(self):
        return str(self.user)