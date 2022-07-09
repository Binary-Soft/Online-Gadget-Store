from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse

from . models import Category, Product, WishList, Order

# Create your views here.

# for home page
class HomeView(TemplateView):
    template_name = "productstemplate/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all().order_by('category_name')
        context['products'] = Product.objects.all().order_by('-datatime')[:9]
        return context


# Category Products
class SpecificCategoryAllProducts(ListView):
    template_name = "productstemplate/specificeproducts.html"
    paginate_by = 20
    paginate_orphans = 1
    
    context_object_name = 'products'

    def get_queryset(self, *args, **kwargs):
        category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        products = Product.objects.filter(category=category).all().order_by('-datatime')
        return products
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, slug=self.kwargs.get('slug'))  
        return context


# for single product details
class ProductDetailView(DetailView):
    template_name = "productstemplate/singleproduct.html"
    model = Product


# for product add to cart
class AddToCart(LoginRequiredMixin, View):
    login_url = "/user/login/"
    template_name = "productstemplate/addcart.html"

    def post(self, *args, **kwargs):
        id = self.request.POST['productID']
        product = get_object_or_404(Product, pk=id)
        user = User.objects.get(email=self.request.user)

        if WishList.objects.filter(user=user, product=product).exists() == True:
            wishlist = WishList.objects.get(user=user, product=product)
            wishlist.quantity += 1
            wishlist.total_price += product.price
        else:
            wishlist = WishList(user=user, product=product, quantity=1, total_price=product.price)
        wishlist.save()
        return HttpResponseRedirect(reverse('add-to-cart'))


    def get(self, *args, **kwargs):
        user = User.objects.get(email=self.request.user)
        wishlist = WishList.objects.filter(user=user).order_by('-datatime')
        total_price = 0
        for product in wishlist:
            total_price += product.total_price
        userwishlist = {'wishlist': wishlist, 'totalprice': total_price}
        return render(self.request, self.template_name, userwishlist)


# delete user wishlist
class DeleteWishList(LoginRequiredMixin, View):
    login_url = "/user/login/"

    def get(self, *args, **kwargs):
        id = kwargs['pk']
        user = User.objects.get(email=self.request.user)
        wishlist = WishList.objects.get(user=user, pk=id)
        wishlist.delete()
        return HttpResponseRedirect(reverse('add-to-cart'))


# user all orders
class UserOrderView(LoginRequiredMixin, ListView):
    login_url = "/user/login"
    template_name = 'productstemplate/userorders.html'
    paginate_by = 20
    paginate_orphans = 5
    context_object_name = 'orders'

    def get_queryset(self, *args, **kwargs):
        user = User.objects.get(email=self.request.user)
        allOrders = Order.objects.filter(user=user).order_by('-datatime')
        return allOrders


'''
admin
123

bdskynet75@gmail.com
Tintinbd12
'''