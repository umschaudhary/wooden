from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from items.models import Item
from settings.models import FiscalYear
from users.models import User, GuestEmail


# Create your models here.

class Rating(models.Model):
    fiscal_year = models.ForeignKey(FiscalYear, on_delete=models.DO_NOTHING, related_name='ratings')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.DO_NOTHING)
    guest_user = models.ForeignKey(GuestEmail, null=True, blank=True, on_delete=models.DO_NOTHING)
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING, related_name='ratings')
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ratings_rating'

    def __str__(self):
        return '{}'.format(self.item.name)
