# Create your views here.
from django.http import HttpResponse

from items.models import Item
from ratings.models import Rating
from settings.models import FiscalYear
from users.models import GuestEmail


def rating_create(request, slug):
    try:
        item = Item.objects.get(slug=slug)
    except Item.DoesNotExist:
        item = None
    if item:
        if request.method == 'POST':
            if request.is_ajax():
                data = request.POST['rating']
                if data:
                    if request.user.is_authenticated:
                        if request.user.is_customer():
                            try:
                                rating = Rating.objects.get(item=item, user=request.user)
                            except Rating.DoesNotExist:
                                rating = None
                            if not rating:
                                rating = Rating()
                                rating.fiscal_year = FiscalYear.get_active_fiscal_year()
                                rating.item = item
                                rating.rating = data
                                rating.user = request.user
                                rating.save()
                                astr = data
                                return HttpResponse(astr)
                            else:
                                astr = "<html><b> you sent an ajax post request </b> <br> returned data: %s</html>" % data
                                return HttpResponse(astr)
                    else:
                        session = request.session['guest_email_id']
                        if session:
                            try:
                                guest_user = GuestEmail.objects.get(id=session)
                            except GuestEmail.DoesNotExist:
                                guest_user = None
                            try:
                                rating = Rating.objects.get(item=item, guest_user=guest_user)
                            except Rating.DoesNotExist:
                                rating = None

                            if not rating:
                                rating = Rating()
                                rating.fiscal_year = FiscalYear.get_active_fiscal_year()
                                rating.item = item
                                rating.rating = data
                                rating.guest_user = guest_user
                                rating.save()
                                astr = "<html><b> you sent an ajax post request </b> <br> returned data: %s</html>" % data
                                return HttpResponse(astr)
                            else:
                                astr = "<html><b> you sent an ajax post request </b> <br> returned data: %s</html>" % data
                                return HttpResponse(astr)

    return HttpResponse('created')
