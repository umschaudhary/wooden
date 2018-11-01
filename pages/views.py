from datetime import date

from django.http import HttpResponseRedirect , HttpResponse
from django.shortcuts import redirect, render, reverse

from settings.models import FiscalYear, TypeOfHouse, WardNumber, WardStaff
from settings.models.ward_no import WardSession
from users.models import Sidebar


# Create your views here.


def home(request):
    context = {}

    user = request.user
    active_fiscal_year = FiscalYear.get_active_fiscal_year()
    ward_numbers = WardNumber.objects.all_active().count()
    houses = TypeOfHouse.objects.all_active().count()
    wardstaffs = WardStaff.objects.all_active()
    context['wardstaffs'] = wardstaffs
 
    if active_fiscal_year is None:
        if user.is_authenticated and user.is_admin:
            return HttpResponseRedirect(reverse('fiscal_years:list'))

    if not ward_numbers > 0:
        if user.is_authenticated and user.is_admin:
            return HttpResponseRedirect(reverse('ward_numbers:list'))

    if not houses > 0:
        if user.is_authenticated and user.is_admin:
            return HttpResponseRedirect(reverse('type_of_houses:list'))

    if user.is_authenticated :
        sidebar_obj, new_obj = Sidebar.objects.new_or_get(request)
        if user.is_superuser():
            template_name = 'pages/admin_dashboard.html'
        elif user.is_wardstaff():
            template_name = 'pages/ward_staff_dashboard.html'
        else:
            pass
    else:
        if request.method == 'POST':
            ward_no =  (request.POST.get('ward_no'))
            if ward_no:
                ward = WardNumber.objects.get(id=ward_no)
            else:
                ward = None
            ward_session_obj, new_obj = WardSession.objects.new_or_get(request)
            ward_session_obj.ward_no = ward
            ward_session_obj.save()
            context['ward_session'] = ward_session_obj
            return redirect('user_home')
        
        template_name = 'pages/user_dashboard.html'

    context['year'] = date.today().year
    context['ward_numbers'] = WardNumber.objects.all_active()
    return render(request, template_name, context)


def user_home(request):
    ward_session_obj, new_obj = WardSession.objects.new_or_get(request)
    if ward_session_obj.ward_no == None:
        return redirect('home')

    context = {}
    return render(request,'pages/home.html',context)