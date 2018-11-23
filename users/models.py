from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
from django.db import models
from model_utils import Choices

USER_ROLES = Choices(
    'admin',
    'provider',
    'customer',
)

GENDER_TYPES = Choices(
    'male',
    'female',
    'confidential',
)


class UserManager(BaseUserManager):
    def create_user(self, email, full_name=None, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")

        user_obj = self.model(
            email=self.normalize_email(email),
            full_name=full_name
        )
        user_obj.set_password(password)  # change user password
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, full_name=None, password=None):
        user = self.create_user(
            email,
            full_name=full_name,
            password=password,

        )
        user.role = 'provider'
        return user

    def create_superuser(self, email, full_name=None, password=None):
        user = self.create_user(
            email,
            full_name=full_name,
            password=password,

        )

        user.is_staff = True
        user.is_admin = True
        user.role = 'admin'
        user.save()
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=100, choices=USER_ROLES, default=USER_ROLES.admin)
    is_active = models.BooleanField(default=True)  # can login
    is_staff = models.BooleanField(default=False)  # staff user non superuser
    is_admin = models.BooleanField(default=False)  # superuser
    timestamp = models.DateTimeField(auto_now_add=True)
    # confirm     = models.BooleanField(default=False)
    # confirmed_date     = models.DateTimeField(default=False)

    USERNAME_FIELD = 'email'  # username
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = []  # ['full_name'] #python manage.py createsuperuser

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.email

    def get_short_name(self):
        if self.full_name:
            return self.full_name
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def has_permission(self):
        return self.active and self.staff

    def is_superuser(self):
        return self.role == USER_ROLES.admin

    def is_provider(self):
        return self.role == USER_ROLES.provider

    def is_customer(self):
        return self.role == USER_ROLES.customer

    class Meta:
        db_table = 'users_user'


class GuestEmail(models.Model):
    email = models.EmailField()
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'users_guest_email'


class SideBarManager(models.Manager):
    def new_or_get(self, request, ):
        sidebar_id = request.session.get('sidebar_id', None)
        qs = self.get_queryset().filter(id=sidebar_id)
        if qs.count() == 1:
            new_obj = False
            print('sidebar exist')
            sidebar_obj = qs.first()
            if request.user.is_authenticated and sidebar_obj.user == None:
                sidebar_obj.user = request.user
                sidebar_obj.save()
        else:
            sidebar_obj = Sidebar.objects.new_sidebar(user=request.user)
            new_obj = True
            request.session['sidebar_id'] = sidebar_obj.id
            request.session['sidebar_id_status'] = sidebar_obj.is_opened
        return sidebar_obj, new_obj

    def new_sidebar(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)


class Sidebar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_opened = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = SideBarManager()

    def __str__(self):
        return '{}'.format(self.id)

    class Meta:
        db_table = 'users_sidebar'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    phone_number = models.CharField(max_length=10, error_messages={'max_length': 'Only 10 Digits Allowed'})
    pic = models.ImageField()
    gender = models.CharField(max_length=100, choices=GENDER_TYPES, default=GENDER_TYPES.confidential)
    address_line_1 = models.CharField(max_length=120)
    address_line_2 = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=120)
    country = models.CharField(max_length=120, default='Nepal')
    postal_code = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'users_user_profile'

    def __str__(self):
        return '{}'.format(self.user.full_name)

    def get_address(self):
        return "{line1}\n{line2}\n{city}\n, {postal}\n{country}".format(
            line1=self.address_line_1,
            line2=self.address_line_2 or "",
            city=self.city,
            postal=self.postal_code,
            country=self.country
        )
