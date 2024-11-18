from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):

    groups = models.ManyToManyField(Group, blank=True,  related_name='customuser_set')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='customuser_set')
    pass