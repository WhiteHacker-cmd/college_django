from django.contrib import admin
from .models import Player
# from django.contrib.auth.admin import UserAdmin
# from .models import User

# # Register your models here.

# class CustomAdmin(UserAdmin):
#     search_fields = ('email','username', 'first_name', 'last_name')
#     ordering = ('email',)

# admin.site.register(User, CustomAdmin)
admin.site.register(Player)