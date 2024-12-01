from django.db import models
from django.contrib.auth.models import User

class TelegramUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telegram_id = models.IntegerField(unique=True)
    telegram_username = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=260, blank=True, null=True)
    def __str__(self):
        return self.telegram_username or str(self.telegram_id)
