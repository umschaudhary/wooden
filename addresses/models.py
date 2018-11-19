from django.db import models
from billings.models import BillingProfile
from model_utils import Choices

ADDRESS_TYPES = Choices(
    'billing',
    'shipping',
)


class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, related_name='addresses', on_delete=models.CASCADE)
    address_type = models.CharField(max_length=120, choices=ADDRESS_TYPES)
    address_line_1 = models.CharField(max_length=120)
    address_line_2 = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=120)
    country = models.CharField(max_length=120, default='Nepal')
    postal_code = models.CharField(max_length=120)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}-{}'.format(self.billing_profile, self.address_type)

    def get_address(self):
        return "{line1}\n{line2}\n{city}\n, {postal}\n{country}".format(
            line1=self.address_line_1,
            line2=self.address_line_2 or "",
            city=self.city,
            postal=self.postal_code,
            country=self.country
        )

    class Meta:
        db_table = 'addresses_address'
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
