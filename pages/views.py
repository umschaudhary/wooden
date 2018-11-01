from datetime import date

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, reverse

from settings.models import FiscalYear
from users.models import Sidebar


# Create your views here.


def home(request):
    context = {}
    user = request.user
    active_fiscal_year = FiscalYear.get_active_fiscal_year()
    
 
    if user.is_authenticated :
        sidebar_obj, new_obj = Sidebar.objects.new_or_get(request)
        if user.is_superuser():
            template_name = 'pages/admin_dashboard.html'
        elif user.is_provider():
            template_name = 'pages/provider_dashboard.html'
        else:
            pass

    context['year'] = date.today().year
    return render(request, template_name, context)
