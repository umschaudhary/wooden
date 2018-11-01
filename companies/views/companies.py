from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


@login_required
@admin_required
def companies(request):
    context = {}
    
    return render(request, template_name, context)