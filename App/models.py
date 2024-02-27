from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    surname = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    age = models.IntegerField(null=True)
        
    def __str__(self):
            return f"{self.user.username}'s Profile"

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  
    
    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}: {self.text[:50]}"

class Chat(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name
      
class Group(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User)
    admins = models.ManyToManyField(User, related_name='admin_groups')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name