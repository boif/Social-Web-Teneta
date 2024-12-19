"""
This module defines the models used in profile app.

Models:
    - Profile
"""

from django.db import models
from django.contrib.auth import get_user_model

class Profile(models.Model):
    """
    Represents the profile model.
    """
    User = get_user_model()
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profile_pic = models.ImageField(upload_to='profile', default='profile/default.png', blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    subscription = models.ManyToManyField('self', symmetrical=False, blank=True)

    def __str__(self):
        """
        Returns the string representation of the profile model.
        """
        return str(self.user)
