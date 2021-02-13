from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from main_app.models import *


# class CustomUserAdmin(UserAdmin):
#     ordering = ('rating_points',)
#     list_display = (
#         'email', 'first_name', 'last_name', 'rating_points', 'photo', 'date_joined', 'last_login', 'first_name',
#         'is_admin', 'is_active', 'is_staff',
#     )
#     search_fields = ('email', 'first_name', 'last_name',)
#     readonly_fields = ('date_joined',)
#
#     filter_horizontal = ()
#     list_filter = ()
#     fieldsets = ()


admin.site.register(CustomUser)#, CustomUserAdmin)
admin.site.register(Record)
