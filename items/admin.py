from django.contrib import admin

from items.models import Item, StockRecord


# Register your models here.
admin.site.register(Item)
admin.site.register(StockRecord)