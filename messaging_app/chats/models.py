from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
  pass

class Conversation(models.Model):
  users =  models.ManyToManyField('User', related_name='conversation')
  created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
  sender = models.ForeignKey('User', on_delete=models.CASCADE)
  Conversation = models.ForeignKey('conversation', on_delete=models.CASCADE, realted_name='messages')
  content = models.TextField()
  timestamp = models.DateTimeField(auto_now_add=True)