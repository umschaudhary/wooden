
from django.contrib import admin
from django.contrib.auth.models import Group
from users.models import User, GuestEmail, Sidebar, UserProfile


admin.site.register(GuestEmail)
admin.site.register(Sidebar)
admin.site.register(User)
admin.site.register(UserProfile)
