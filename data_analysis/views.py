from django.shortcuts import render


# Create your views here.

def orders(request):
    context = {}
    template_name = 'data_analysis/orders.html'
    return render(request, template_name, context)
