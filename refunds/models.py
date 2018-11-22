from django.db import models

from billings.models import BillingProfile
from categories.models import Category
from companies.models import Company
from ecommerce.utils import CustomModelQuerySet, CustomModelManager
from items.models import Item
from orders.models import OrderItem


class RefundPolicy(models.Model):
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name='refunds')
    provider = models.ForeignKey(Company, on_delete=models.DO_NOTHING, related_name='refunds')
    validity = models.IntegerField()
    cover = models.CharField(max_length=160, error_messages={'max_length': 'Should be of 160 Characters'})
    type_acceptance = models.CharField(max_length=160, error_messages={'max_length': 'Should be of 160 Characters'})
    description = models.TextField()
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomModelManager.from_queryset(CustomModelQuerySet)()

    class Meta:
        db_table = 'refunds_refund_policy'

    def __str__(self):
        return '{}'.format(self.category)


class RefundRequest(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.DO_NOTHING)
    order_item = models.ForeignKey(OrderItem, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(default=1)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'refunds_refund_request'

    def __str__(self):
        return '{}'.format(self.order_item.item.name)
