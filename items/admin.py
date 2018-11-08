from django.contrib import admin

from items.models import Item, ItemImage, StockRecord


# Register your models here.
admin.site.register(Item)
admin.site.register(StockRecord)
admin.site.register(ItemImage)