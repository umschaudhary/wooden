from items.models import Item
from django.http import JsonResponse, HttpResponse
from comments.models import Comment
from settings.models import FiscalYear
import json
from django.core import serializers

def comment_create(request, slug):
    try:
        item = Item.objects.get(slug=slug)
    except Item.MultipleObjectsReturned:
        item = item.objects.filter(slug=slug).last()
    except Item.DoesNotExist:
        item = None
    if request.method == 'POST':   
        if request.user.is_authenticated and request.user.is_customer():
            response_data = {}
            data = request.POST['comment']
            comment = Comment()
            comment.comment = data
            comment.fiscal_year = FiscalYear.get_active_fiscal_year()
            comment.item = item
            comment.user = request.user
            comment.save()

            response_data['result'] = 'Create post successful!'
            response_data['postpk'] = str(comment.pk)
            response_data['comment'] = str(comment.comment)
            response_data['created'] = str(comment.created_at)
            response_data['image'] = str(request.user.userprofile.pic)
            response_data['author'] = str(comment.user.full_name)
            return JsonResponse(response_data)
    else:
        return JsonResponse({'data':'hello owrld'})


