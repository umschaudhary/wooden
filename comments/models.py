from django.db import models

from ecommerce.utils import CustomModelManager, CustomModelQuerySet
from items.models import Item
from settings.models import FiscalYear
from users.models import GuestEmail, User


# Create your models here.

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='comments', null=True, blank=True)
    guest_user = models.ForeignKey(GuestEmail, on_delete=models.DO_NOTHING, related_name='comments', null=True,
                                   blank=True)
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING, related_name='comments')
    fiscal_year = models.ForeignKey(FiscalYear, on_delete=models.DO_NOTHING, related_name='comments')
    comment = models.TextField()
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomModelManager.from_queryset(CustomModelQuerySet)()

    class Meta:
        db_table = 'comments_comment'

    def __str__(self):
        if not self.user == None:
            return '{}'.format(self.user.email)
        elif not self.guest_user == None:
            return '{}'.format(self.guest_user.email)
        else:
            return 'random '
