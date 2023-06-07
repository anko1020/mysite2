from django.contrib import admin

from . import models

admin.site.register(models.Account)
admin.site.register(models.Seat)
admin.site.register(models.CheckSheet)
admin.site.register(models.ItemMenu)
admin.site.register(models.Item)
admin.site.register(models.SheetAccountRelation)
