from companies.models import Company
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from ecommerce import settings
import os
from categories.models import Category
from ecommerce.utils import CustomModelManager, CustomModelQuerySet, \
    unique_slug_generator


# Create your models here.

class Item(models.Model):
    provider = models.ForeignKey(Company, related_name='items', on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category, related_name='items', on_delete=models.DO_NOTHING)
    slug = models.SlugField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=120,error_messages={'max_length':'Length Shouldnot be longer than 120 characters'})
    description = models.TextField()
    available = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomModelManager.from_queryset(CustomModelQuerySet)()

    class Meta:
        db_table = 'items_item'
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    # def get_absolute_url(self, *args, **kwargs):
    #     return reverse('items:item_detail_slug', kwargs={"slug": self.slug})



def item_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(item_pre_save_receiver, sender=Item)


class StockRecord(models.Model):
    item = models.OneToOneField(Item, related_name='stock_record', on_delete=models.DO_NOTHING)
    price_excl_tax = models.DecimalField(max_digits=19, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=19, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    quantity = models.PositiveIntegerField()
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    class Meta:
        db_table = 'items_stock_record'
        verbose_name = 'Stock Record'
        verbose_name_plural = 'Stock Records '

    def __str__(self):
        return self.item.name

def stock_discount_price_calculation(sender, instance , *args, **kwargs):
    price = instance.price_excl_tax
    discount_percent = instance.discount_percentage
    if discount_percent:
        discount = (discount_percent/100)*price
        instance.discounted_price = price - discount

pre_save.connect(stock_discount_price_calculation, sender=StockRecord)



class ItemImage(models.Model):
    item = models.ForeignKey(Item, related_name="item_images", on_delete=models.DO_NOTHING)
    document = models.FileField()

    class Meta:
        db_table = "items_item_image"
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    def __str__(self):
        return self.item.name

