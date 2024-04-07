from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profile_pic = models.ImageField(upload_to='profile', default='profile/default.png', blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.user)

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    subscribed_to = models.ForeignKey(ser, on_delete=models.CASCADE, related_name='subscribers')