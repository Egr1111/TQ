from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    invite_code = models.CharField(max_length=255, null=True)
    invited = models.ManyToManyField("User", blank=True, related_name="Присоединенные")
    last_code = models.DateTimeField(auto_now_add=True, auto_created=True, verbose_name="Время последнего сообщения", blank=True)
