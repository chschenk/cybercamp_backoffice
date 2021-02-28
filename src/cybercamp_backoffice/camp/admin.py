from django.contrib import admin
from cybercamp_backoffice.camp.models import User, Map


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    list_display = ('organization', 'world', 'room')
