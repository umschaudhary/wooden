from django.db import models

from items.models import Item


class RefundPolicy(models.Model):
    item = models.OneToOneField(Item, on_delete=models.DO_NOTHING, related_name='refunds')
    validity = models.IntegerField()
    cover = models.CharField(max_length=160, error_messages={'max_length': 'Should be of 160 Characters'})
    type_acceptance = models.CharField(max_length=160, error_messages={'max_length': 'Should be of 160 Characters'})
    description = models.TextField()

    class Meta:
        db_table = 'refunds_refund_policy'

    def __str__(self):
        return '{}'.format(self.item)
