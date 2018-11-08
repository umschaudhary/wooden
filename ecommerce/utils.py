from django.db import models

import random
import string

from django.utils.text import slugify

class CustomModelQuerySet(models.query.QuerySet):
    
    def inactive(self, *args, **kwargs):
        return self.filter(is_deleted=True)

    def active(self, *args, **kwargs):
        return self.filter(is_deleted=False)


class CustomModelManager(models.Manager):

    def all_active(self, *args, **kwargs):
        return self.get_queryset().active().order_by('-id')




def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_order_id_generator(instance):
    order_new_id = random_string_generator()
    klass = instance.__class__
    qs_exist = klass.objects.filter(order_id=order_new_id).exists()
    if qs_exist:
        return unique_order_id_generator(instance)
    return order_new_id


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name)
    klass = instance.__class__
    qs_exist = klass.objects.filter(slug=slug).exists()
    if qs_exist:
        new_slug = '{}-{}'.format(slug, random_string_generator(size=4))
        return unique_slug_generator(instance, new_slug)
    return slug
