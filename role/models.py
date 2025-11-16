# role/models.py
from django.db import models
from login.models import TimeStampedModel  # inherit audit fields

class Role(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "user_roles" 
