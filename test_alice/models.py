from datetime import timezone

from django.db import models


class Role(models.TextChoices):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Session(models.Model):
    user_id = models.CharField(max_length=100)
    is_open = models.BooleanField(default=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    thinking = models.BooleanField(null=True, blank=True)
    waiting_step = models.IntegerField(null=True, blank=True)

    def close(self):
        """Закрыть сессию — обновить флаг и поставить время завершения"""
        self.is_open = False
        self.ended_at = timezone.now()
        self.save()


class ChatHistory(models.Model):
    message = models.TextField()
    role = models.CharField(max_length=10, choices=Role)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
