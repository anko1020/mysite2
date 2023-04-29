from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone


class Account(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    is_working = models.BooleanField(default=False)

    start_time = models.DateTimeField(verbose_name="開始時間")
    end_time = models.DateTimeField(verbose_name="終了時間")

    start_overtime = models.CharField(max_length=20, null=True)
    end_overtime = models.CharField(max_length=20, null=True)
    
    is_sending = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username
