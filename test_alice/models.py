from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=100)

class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_open = models.BooleanField(default=False)

class ChatHistory(models.Model):
    message = models.TextField()
    role = models.CharField(max_length=100)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
