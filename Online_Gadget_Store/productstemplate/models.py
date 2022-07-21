from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
import datetime

# Create your models here.

class Notice(models.Model):
    announcement = models.TextField(max_length=255)

    def __str__(self):
        return self.announcement[:20] + '...'


class HeadLineMessage(models.Model):
    name = models.CharField(max_length=255, default='', blank=True, help_text='Imagen name or any Messages')
    logo = models.ImageField('Picture', upload_to='HeadLine', help_text='Upload the Home pages Cover image or Any Message')

    def __str__(self):
        return self.name.title()


class Category(models.Model):
    category_name = models.CharField(max_length=20, unique=True)
    logo = models.ImageField(upload_to='Category')
    slug = models.SlugField(unique="True", help_text="Slug is a field in autocomplete mode, but if you want you can modify its contents")

    def __str__(self):
        return self.category_name


class Brand(models.Model):
    brand_name = models.CharField(max_length=40, null=True, blank=True, unique=True)

    def __str__(self):
        return self.brand_name


class Product(models.Model):
    product_name = models.CharField(max_length=50, blank=False, help_text='Add Product Model Name or Product Name.')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default="", blank=True, related_name="Products")
    brand_name = models.ForeignKey(Brand, on_delete=models.CASCADE, default="", blank=True, related_name="Products")
    specification = models.CharField(max_length=400, blank=True, default="")
    price = models.FloatField(blank=False, default=0.00, validators=[MinValueValidator(0.0)], help_text='Price Can not be Less than Zero.')
    quantity = models.PositiveBigIntegerField(default=0)
    inStock = models.BooleanField(default=True)
    datatime = models.DateTimeField(auto_now_add=True)
    warranty = models.CharField(max_length=50, blank=True)
    image1 = models.ImageField(upload_to='Product Images')
    image2 = models.ImageField(upload_to='Product Images', blank=True)
    image3 = models.ImageField(upload_to='Product Images', blank=True)
    image4 = models.ImageField(upload_to='Product Images', blank=True)

    class Meta:
        unique_together = [['category', 'brand_name', 'product_name', 'specification'] ]
    
    def __str__(self):
        return self.product_name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product")
    shipping_address = models.CharField(max_length=255)
    quantity = models.PositiveBigIntegerField(default=0)
    sub_total_price = models.FloatField(default=0.0)
    total_price = models.FloatField(default=0.0)
    phone = models.CharField(max_length=15)
    datatime = models.DateTimeField(auto_now_add=True)
    is_last = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user) + " | " + str(self.product)


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="products")
    quantity = models.PositiveBigIntegerField(default=0)
    total_price = models.FloatField(default=0.0)
    datatime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user) + "  |  " + str(self.product)
    