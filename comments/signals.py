from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from comments.models import Comment
from settings.models import FiscalYear



