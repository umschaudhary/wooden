from django.db import models

class CustomModelQuerySet(models.query.QuerySet):
    
    def inactive(self, *args, **kwargs):
        return self.filter(is_deleted=True)

    def active(self, *args, **kwargs):
        return self.filter(is_deleted=False)


class CustomModelManager(models.Manager):

    def all_active(self, *args, **kwargs):
        return self.get_queryset().active().order_by('-id')
