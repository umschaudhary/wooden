from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from orders.models import Order
from users.decorators import provider_required
from users.models import User


@api_view(['GET'])
def cartdata(request, format=None):
    user = request.user
    if user.is_authenticated and user.is_provider():
        orders = Order.objects.filter(is_deleted=False,
                                      order_items__item__provider=user.company_admin.company).count()
    else:
        orders = Order.objects.none()
    labels = [
        "orders",
    ]
    default_items = [
        orders,

    ]
    data = {
        'labels': labels,
        'defaultData': default_items,

    }
    return Response(data)


@login_required
@provider_required
def char_data(request):
    user = request.user
    fiscal_year = request.active_fiscal_year
    if user.is_authenticated and user.is_provider():
        default_items = [
        ]
    for i in range(1, 13):
        orders = Order.objects.filter(is_deleted=False,
                                      order_items__item__provider=user.company_admin.company,
                                      date__month=i,
                                      fiscal_year=fiscal_year).distinct().count()

        default_items.append(orders)

    labels = [
        "Jan", "Feb", "March", "Apr", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    data = {
        'labels': labels,
        'defaultData': default_items,

    }
    return JsonResponse(data)


@api_view(['GET'])
def customer_count(request, format=None):
    labels = [
        "Jan", "Feb", "March", "Apr", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]
    default_items = [

    ]
    for i in range(1, 13):
        customers = User.objects.filter(is_active=True, role='customer', timestamp__month=i).count()
        default_items.append(customers)
    data = {
        'labels': labels,
        'defaultData': default_items,
    }
    return Response(data)
