from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from orders.models import Order
from users.decorators import provider_required


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
        jan = Order.objects.filter(is_deleted=False,
                                   order_items__item__provider=user.company_admin.company,
                                   date__month=1,
                                   fiscal_year=fiscal_year).distinct().count()
        feb = Order.objects.filter(is_deleted=False,
                                   order_items__item__provider=user.company_admin.company,
                                   date__month=2,
                                   fiscal_year=fiscal_year).distinct().count()
        mar = Order.objects.filter(is_deleted=False,
                                   order_items__item__provider=user.company_admin.company,
                                   date__month=3,
                                   fiscal_year=fiscal_year
                                   ).distinct().count()
        apr = Order.objects.filter(is_deleted=False,
                                   order_items__item__provider=user.company_admin.company,
                                   date__month=4,
                                   fiscal_year=fiscal_year
                                   ).distinct().count()
        may = Order.objects.filter(is_deleted=False,
                                   order_items__item__provider=user.company_admin.company,
                                   date__month=5,
                                   fiscal_year=fiscal_year
                                   ).distinct().count()
        june = Order.objects.filter(is_deleted=False,
                                    order_items__item__provider=user.company_admin.company,
                                    date__month=6,
                                    fiscal_year=fiscal_year
                                    ).distinct().count()
        july = Order.objects.filter(is_deleted=False,
                                    order_items__item__provider=user.company_admin.company,
                                    date__month=7,
                                    fiscal_year=fiscal_year
                                    ).distinct().count()
        aug = Order.objects.filter(is_deleted=False,
                                   order_items__item__provider=user.company_admin.company,
                                   date__month=8,
                                   fiscal_year=fiscal_year
                                   ).distinct().count()
        sep = Order.objects.filter(is_deleted=False,
                                   order_items__item__provider=user.company_admin.company,
                                   date__month=9,
                                   fiscal_year=fiscal_year
                                   ).distinct().count()
        october = Order.objects.filter(is_deleted=False,
                                       order_items__item__provider=user.company_admin.company,
                                       date__month=10,
                                       fiscal_year=fiscal_year
                                       ).distinct().count()
        nov = Order.objects.filter(is_deleted=False,
                                   order_items__item__provider=user.company_admin.company,
                                   date__month=11,
                                   fiscal_year=fiscal_year
                                   ).distinct().count()
        dec = Order.objects.filter(is_deleted=False,
                                   order_items__item__provider=user.company_admin.company,
                                   date__month=12,
                                   fiscal_year=fiscal_year

                                   ).distinct().count()

    labels = [
        "Jan", "Feb", "March", "Apr", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]
    default_items = [
        jan,
        feb,
        mar,
        apr,
        may,
        june,
        july,
        aug,
        sep,
        october,
        nov,
        dec

    ]
    data = {
        'labels': labels,
        'defaultData': default_items,

    }
    return JsonResponse(data)
