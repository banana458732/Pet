from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):

    groups = models.ManyToManyField(Group, blank=True,  related_name='customuser_set')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='customuser_set')
    
    address = models.CharField(
        verbose_name='住所',
        max_length=30,
        null=True,blank=True
    )

    phone_number = models.CharField(
        verbose_name='電話番号',
        max_length=128,
        null=True,blank=True
    )


    

