from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone


class Account(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    is_working = models.BooleanField(default=False)

    start_time = models.DateTimeField(verbose_name="開始時間")
    end_time = models.DateTimeField(verbose_name="終了時間")

    start_overtime = models.CharField(max_length=20, null=True)
    end_overtime = models.CharField(max_length=20, null=True)

    is_sending = models.BooleanField(default=False)

    staff_drink = models.IntegerField(default=0)
    staff_bottle = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class CheckSheet(models.Model):
    total_fee = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    how_cash = models.CharField(max_length=20, null=True)

    asign = models.BooleanField(default=False)

    client_name = models.CharField(max_length=20, null=True)
    client_num = models.IntegerField(default=0)

    start_time = models.DateTimeField(verbose_name="来店時間")
    end_time = models.DateTimeField(verbose_name="退店時間")

    start_overtime = models.CharField(max_length=20, null=True)
    end_overtime = models.CharField(max_length=20, null=True)

    staff = models.ManyToManyField("Account")

    memo_str = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return self.client_name


class ItemMenu(models.Model):
    menu = models.CharField(max_length=10, null=True)
    def __str__(self):
        return self.menu


class Item(models.Model):
    item_name = models.CharField(max_length=20, null=True)
    staff =  models.CharField(max_length=20, null=True)
    item_num = models.IntegerField()
    item_cost = models.IntegerField()

    checkSheet = models.ForeignKey(CheckSheet, on_delete=models.CASCADE)
    Menu = models.ForeignKey(ItemMenu, on_delete=models.CASCADE)

    def __str__(self):
        return self.item_name


class Seat(models.Model):
    Seat_ID = models.CharField(max_length=10, null=True)
    CheckSheet = models.ForeignKey(CheckSheet, on_delete=models.CASCADE)

    attr = models.CharField(max_length=3, null=True)
    
    pos_x = models.IntegerField(default=0)
    pos_y = models.IntegerField(default=0)

    is_use = models.BooleanField(default=False)

    def __str__(self):
        return self.Seat_ID
    
