from django.db import models
from django.core.validators import EmailValidator
from users.models import User
from ecommerce.utils import CustomModelManager, CustomModelQuerySet
   
# Create your models here.


class Company(models.Model):
    name = models.CharField(
        max_length=64,
        error_messages={
            'max_length': "Length Shouldn't exceed 64 characters "}
    )

    address = models.CharField(
        max_length=64,
        error_messages={'max_length': "Length Shouldn't exceed 64 characters"}
    )
    postal = models.CharField(
        max_length=20,
        error_messages={'max_length': "Length Shouldn't exceed 20 characters"}
    )
    city = models.CharField(
        max_length=64,
        error_messages={'max_length': "Length Shouldn't exceed 64 characters"}
    )
    email = models.EmailField(validators=[EmailValidator(message="Invalid Email Address")])

    phone_number =  models.CharField(
        max_length=15,
        error_messages={
            'max_length': "Length Shouldn't exceed 15 digits "}
    )

    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomModelManager.from_queryset(CustomModelQuerySet)()


    def __str__(self):
        return self.name

    class Meta:
        db_table = 'companies_company'

class CompanyAdmin(models.Model):
    full_name = models.CharField(max_length=120,error_messages={'max_length':'Length Shouldnot exceed 120 Characters'})
    user = models.OneToOneField(User, related_name='company_admin', on_delete=models.DO_NOTHING,null=True, blank=True)
    company = models.ForeignKey(Company,related_name='company_admins', on_delete=models.DO_NOTHING, null=True, blank=True)
    email = models.EmailField(validators=[EmailValidator(message="Invalid Email Address")])
    password = models.CharField(max_length = 20)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomModelManager.from_queryset(CustomModelQuerySet)()
    
    def __str__(self):
        return '{}'.format(self.full_name)

    class Meta:
        db_table = 'companies_company_admin'
        verbose_name = 'Company Admin'
        verbose_name_plural = 'Company Admins'