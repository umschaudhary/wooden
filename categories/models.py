from django.db import models

from ecommerce.utils import CustomModelManager, CustomModelQuerySet


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=120, error_messages={'max_length':'Length Should Not Exceed 120 Characters '})
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