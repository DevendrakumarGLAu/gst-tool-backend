# registration/models.py
from django.db import models
from django.contrib.auth.hashers import make_password

from core.models import TimeStampedModel
from role.models import Role

class UserAccount(TimeStampedModel):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    full_name = models.CharField(max_length=100)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="users")
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return f"{self.full_name} ({self.role.name})"
    
    class Meta:
        db_table = "user_registration" 
