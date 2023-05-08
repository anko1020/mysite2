from django.contrib import admin

from .models import Account, Seat, CheckSheet, Client, Item

admin.site.register(Account)
admin.site.register(Seat)
admin.site.register(CheckSheet)
admin.site.register(Client)
admin.site.register(Item)
