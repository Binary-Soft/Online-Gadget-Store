from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class ExtendUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=300)
    phone = models.CharField(max_length=16)
    picture = models.ImageField(upload_to='images')

    def __str__(self):
        return self.user


class Category(models.Model):
    category_name = models.CharField(max_length=20, default="", unique=True)

    def __str__(self):
        return self.category_name


class Brand(models.Model):
    brand_name = models.CharField(max_length=40, null=True, blank=True, unique=True)

    def __str__(self):
        return self.brand_name


class Product(models.Model):
    product_name = models.CharField(max_length=30, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default="", blank=True, related_name="Products")
    brand_name = models.ForeignKey(Brand, on_delete=models.CASCADE, default="", blank=True, related_name="Products")
    specification = models.CharField(max_length=400, blank=True, default="")
    price = models.FloatField(blank=False, default=0.00)
    datatime = models.DateTimeField(auto_now_add=True)
    warranty = models.CharField(max_length=50, blank=True)
    image1 = models.ImageField(upload_to='Product Images')
    image2 = models.ImageField(upload_to='Product Images', blank=True)
    image3 = models.ImageField(upload_to='Product Images', blank=True)

    class Meta:
        unique_together = ['category', 'brand_name']
    
    def __str__(self):
        return self.product_name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product")
    shipping_address = models.CharField(max_length=100)
    quantity = models.PositiveBigIntegerField(default=0)
    total_price = models.FloatField(default=0.0)

    def __str__(self):
        return self.user + " | " + self.product


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="products")
    quantity = models.PositiveBigIntegerField(default=0)
    total_price = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.user) + "  |  " + str(self.product)