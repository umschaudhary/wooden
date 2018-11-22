from django.contrib import admin

from refunds.models import RefundPolicy, RefundRequest

admin.site.register(RefundPolicy)
admin.site.register(RefundRequest)
