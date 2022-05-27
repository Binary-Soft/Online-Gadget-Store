from django.contrib import admin

from .models import (ExtendUser, Category, Brand, Product, Order, WishList)

# Register your models here.

admin.site.register(ExtendUser)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(WishList)