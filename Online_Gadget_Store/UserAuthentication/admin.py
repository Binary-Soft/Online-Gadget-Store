from django.contrib import admin
from . models import (ExtendUser, )


# Register your models here.


@admin.register(ExtendUser)
class ExtendUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'address', ]
    list_filter = ['user', ]