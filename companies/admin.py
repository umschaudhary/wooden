from django.contrib import admin

from companies.models import Company, CompanyAdmin


# Register your models here.
admin.site.register(Company)
admin.site.register(CompanyAdmin)