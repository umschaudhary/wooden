import math
from django.db import models
from django.db.models.signals import pre_save, post_save
from addresses.models import Address
from billings.models import BillingProfile
from carts.models import Cart
from ecommerce.utils import unique_order_id_generator
from items.models import Item
from settings.models import FiscalYear

ORDER_STATUS_CHOICES = (
    ('created ', 'created'),
    ('paid', 'paid'),
    ('shipped', 'shipped'),
    ('refunded', 'refunded'),
)


class OrderManager(models.Manager):
    def new_or_get(self, billing_profile, cart_obj):
        created = False
        qs = self.get_queryset().filter(
            billing_profile=billing_profile,
            cart=cart_obj,
            active=True,
            status='created'
            )
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(
                billing_profile=billing_profile,
                cart=cart_obj
                )
            created = True
        return obj, created

    def get_order(self, billing_profile, cart_obj):
        created = False
        qs = self.get_queryset().filter(
            billing_profile=billing_profile,
            cart=cart_obj,
            active=True,
            status='created'
            )
        if qs.count() == 1:
            obj = qs.first()
            
        return obj


class Order(models.Model):
    fiscal_year = models.ForeignKey(FiscalYear,on_delete=models.DO_NOTHING, related_name='orders')
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE, related_name='orders', null=True,
                                        blank=True)
    shipping_address = models.ForeignKey(Address, related_name="shipping_address", null=True, blank=True,
                                         on_delete=models.CASCADE)
    billing_address = models.ForeignKey(Address, related_name="billing_address", null=True, blank=True,
                                        on_delete=models.CASCADE)
    order_id = models.CharField(max_length=120, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=255, choices=ORDER_STATUS_CHOICES, default='created')
    shipping_total = models.DecimalField(max_digits=19, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=19, decimal_places=2, default=0.00)
    active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = OrderManager()

    def __str__(self):
        return self.order_id

    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = math.fsum([cart_total, shipping_total])
        formatted_total = format(new_total, '.2f')
        self.total = formatted_total
        self.save()

        return new_total

    def check_done(self):
        billing_profile = self.billing_profile
        shipping_address = self.shipping_address
        billing_address = self.billing_address
        total = self.total
        if billing_profile and shipping_address and billing_address and total > 0:
            return True
        return False

    def mark_paid(self):
        if self.check_done():
            self.status = "paid"
            self.save()

        return self.status

    class Meta:
        db_table = 'orders_order'


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    instance.fiscal_year = FiscalYear.get_active_fiscal_year()
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)


pre_save.connect(pre_save_create_order_id, sender=Order)


def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()


post_save.connect(post_save_cart_total, sender=Cart)


def post_save_order(sender, instance, created, *args, **kwargs):
    print('creating')
    if created:
        print('updating___')
        instance.update_total()


post_save.connect(post_save_order, sender=Order)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.DO_NOTHING)
    item = models.ForeignKey(Item, related_name='order_items', on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField()
    total = models.DecimalField(decimal_places=2, max_digits=19)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders_order_item'
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return '{}'.format(self.item.name)
