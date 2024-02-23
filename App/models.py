from django.db import models
from django.contrib.auth.models import User



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True, upload_to='uploads/', null=True)
    bio = models.TextField(blank=True)
    # Добавление друзей
    friends = models.ManyToManyField('self', symmetrical=True, related_name='profile_friends')

    def __str__(self):
        return self.user.username
    
class Message(models.Model):
    sender_id = models.ForeignKey(Profile,on_delete=models.CASCADE)
    
    
    
    
    

