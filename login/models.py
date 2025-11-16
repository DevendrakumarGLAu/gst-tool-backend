from django.db import models

from core.models import TimeStampedModel



# Create your models here.
# class UserAccount(TimeStampedModel):
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=255)
    
#     def __str__(self):
#         return f"{self.email} ({self.id})"
    
#     class Meta:
#         db_table = "user_account" 
        
# class Role(TimeStampedModel):
#     name = models.CharField(max_length=50, unique=True)  # e.g., student, teacher, principal
#     description = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return self.name
