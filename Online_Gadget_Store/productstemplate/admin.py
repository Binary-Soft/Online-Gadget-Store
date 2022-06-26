from django.contrib import admin

from .models import (Category, Brand, Product, Order, WishList)

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("category_name",)}


admin.site.register(Brand)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['category', 'brand_name', 'product_name']
    list_filter = ['category', 'brand_name', ]


admin.site.register(Order)


@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity']
    list_filter = ['user', 'product']