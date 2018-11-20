from django.db import models

from ecommerce.utils import CustomModelManager, CustomModelQuerySet,  unique_slug_generator
from django.db.models.signals import pre_save

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=120, error_messages={'max_length':'Length Should Not Exceed 120 Characters '})
    slug = models.SlugField(max_length=100, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomModelManager.from_queryset(CustomModelQuerySet)()

    class Meta:
        db_table = 'categories_category'
        verbose_name = 'Category'
        

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

def category_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(category_pre_save_receiver, sender=Category)