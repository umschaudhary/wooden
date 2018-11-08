
from django.contrib import admin
from django.contrib.auth.models import Group


from users.models import User, GuestEmail, Sidebar

admin.site.register(User)
admin.site.register(GuestEmail)
admin.site.register(Sidebar)