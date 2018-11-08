from django.db import models
from users.models import User
from items.models import Item


# Create your models here.


class CartManager(models.Manager):

    def new_or_get(self, request, ):
        cart_id = request.session.get('cart_id', None)

        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            print('cart exist')
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user == None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new_cart(user=request.user)
            new_obj = True
            print('card Created')
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

    def new_cart(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=19, decimal_places=2, default=0.00)
    sub_total = models.DecimalField(max_digits=19, decimal_places=2, default=0.00)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CartManager()

    def __str__(self):
        return '{}'.format(self.id)

    class Meta:
        db_table = 'carts_cart'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.DO_NOTHING)
    item = models.ForeignKey(Item, related_name='cart_items', on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField()
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'carts_cart_item'
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'

    def __str__(self):
        return '{}'.format(self.item.name)
#
# def m2m_change_cart_receiver(sender, instance, action, *args, **kwargs):
#     if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
#         products = instance.products.all()
#         total = 0
#         for x in products:
#             total += x.price
#         if instance.sub_total != total:
#             instance.sub_total = total
#             instance.save()
#
#
# m2m_changed.connect(m2m_change_cart_receiver, sender=Cart.products.through)
#
#
# def pre_save_cart_receiver(sender, instance, *args, **kwargs):
#     if instance.sub_total > 0:
#         instance.total = instance.sub_total
#     else:
#         instance.total = 0
#
#
# pre_save.connect(pre_save_cart_receiver, sender=Cart)
