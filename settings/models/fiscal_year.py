from django.db import models
from ecommerce.utils import CustomModelManager, CustomModelQuerySet


class FiscalYear(models.Model):
    name = models.CharField(
        max_length=64,
        error_messages={
            'max_length': 'Length Shouldnot exceed 64 Characters'}
    )
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomModelManager.from_queryset(CustomModelQuerySet)()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'settings_fiscal_year'
        verbose_name = 'Fiscal Year'
        verbose_name_plural = 'Fiscal Years'

    @staticmethod
    def get_active_fiscal_year():
        try:
            fiscal_year = FiscalYear.objects.get(is_active=True, is_deleted=False)
        except FiscalYear.DoesNotExist:
            fiscal_year = None
        return fiscal_year