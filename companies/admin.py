from django.contrib import admin

from companies.models import Company, CompanyAdmin, CompanyCategory


# Register your models here.
admin.site.register(Company)
admin.site.register(CompanyAdmin)
admin.site.register(CompanyCategory)