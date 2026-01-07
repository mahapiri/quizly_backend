from django.contrib.auth.models import User
from django.db import models

# Create your models here.
# class Profile(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profiles')

#     class Meta:
#         verbose_name = "Profile"
#         verbose_name_plural = "Profiles"
        
#     def __str__(self):
#         return self.user.username