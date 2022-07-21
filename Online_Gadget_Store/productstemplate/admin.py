from django.contrib import admin
from django.contrib.auth.models import Group

from .models import (HeadLineMessage, Category, Brand, Product, Order, WishList)

# UnRegister bulitin models here.

admin.site.unregister(Group)


# Register your models here.


admin.site.register(HeadLineMessage)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("category_name",)}


admin.site.register(Brand)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['category', 'brand_name', 'product_name']
    list_filter = ['category', 'brand_name', ]


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'datatime']
    list_filter = ['user', 'datatime']

admin.site.register(Order, OrderAdmin)


@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity']
    list_filter = ['user', 'product']