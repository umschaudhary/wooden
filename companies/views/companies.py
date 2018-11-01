from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from companies.models import Company
from users.decortors import admin_required


# @login_required
# @admin_required
# def companies(request):
#     context = {}
#     objects = Company.objects.all_active()

#     return render(request, template_name, context)