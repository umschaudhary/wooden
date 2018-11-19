
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from users.models import GuestEmail

User = settings.AUTH_USER_MODEL


class BillingProfileManager(models.Manager):

    def new_or_get(self, request):
        user = request.user
        guest_email_id = request.session.get('guest_email_id')
        created = False
        obj = None

        if user.is_authenticated:
            'logged in user checkout; remember payment stuff'
            obj, created = self.model.objects.get_or_create(
                user=user, email=user.email)

        elif guest_email_id is not None:

            'guest user checkout; auto reloads payment stuff'
            guest_email_obj = GuestEmail.objects.get(id=guest_email_id)

            obj, created = self.model.objects.get_or_create(
                email=guest_email_obj.email)
            request.session['guest_email'] = obj.email
        else:
            pass
        return obj, created


class BillingProfile(models.Model):
    user = models.OneToOneField(User, related_name='billing', on_delete=models.CASCADE, null=True,
                                blank=True)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BillingProfileManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'billings_billing_profile'
        verbose_name = 'Billing Profile'
        verbose_name_plural = 'Billing Profiles'


def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)


post_save.connect(user_created_receiver, sender=User)
