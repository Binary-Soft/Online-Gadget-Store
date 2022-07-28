from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Sum


from . models import Notice, Brand, HeadLineMessage, Category, Product, WishList, Order

# Create your views here.

# for home page
class HomeView(TemplateView):
    template_name = "productstemplate/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all().order_by('category_name')
        context['products'] = Product.objects.all().order_by('-datatime')[:9]
        headlines = HeadLineMessage.objects.all()
        context['HeadLineMessages'] = headlines[len(headlines)-3:]
        context['notice'] = Notice.objects.all()[0]
        return context


# all products
class ProductList(ListView):
    template_name = "productstemplate/products.html"

    model = Product
    context_object_name = 'products'
    ordering = ['-datatime']

    paginate_by = 9
    paginate_orphans = 2

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorys'] = Category.objects.all().order_by('-id')
        print(context['categorys'])
        # context['brands'] = Brand.objects.filter(Products__category=context['category']).distinct()
        return context


# for user search
class SearchView(TemplateView):
    template_name = "productstemplate/products.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_search = self.request.GET['product']
        if len(user_search) >= 80 or user_search is None:
            search_result = Product.objects.none()
        else:
            products = Product.objects.all()
            search_result_name = products.filter(product_name__icontains=user_search)
            search_result_category = products.filter(category__category_name__icontains=user_search)
            search_result = search_result_name.union(search_result_category)
        if len(search_result) == 0:
            context['massage'] = user_search[:30] + '...'
        context['products'] = search_result
        return context
        

# Category Products
class SpecificCategoryAllProducts(ListView):
    template_name = "productstemplate/specificeproducts.html"
    paginate_by = 6
    paginate_orphans = 3
    
    context_object_name = 'products'

    def get_queryset(self, *args, **kwargs):
        category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        products = Product.objects.filter(category=category).all().order_by('-datatime')
        return products
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        context['brands'] = Brand.objects.filter(Products__category=context['category']).distinct()
        return context


# filter by category and brand name
class CategoryBrand(SpecificCategoryAllProducts):
    
    def get_queryset(self, *args, **kwargs):
        category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        brand = get_object_or_404(Brand, brand_name=self.kwargs.get('brand'))
        products = Product.objects.filter(category=category, brand_name=brand).all().order_by('-datatime')
        return products



# for single product details
class ProductDetailView(DetailView):
    template_name = "productstemplate/singleproduct.html"
    model = Product


# for product add to cart
class AddToCart(LoginRequiredMixin, View):
    login_url = "/user/login/"
    template_name = "productstemplate/addcartlist.html"

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
        total_price = wishlist.aggregate(Sum('total_price'))
        context = {'wishlist': wishlist, 
        'total_price': total_price.get('total_price__sum') if total_price.get('total_price__sum') is not None else 0}
        return render(self.request, self.template_name, context)


# delete user wishlist
class AddOrDeleteWishList(LoginRequiredMixin, View):
    login_url = "/user/login/"

    # remove a specific product from user wishlist
    def get(self, *args, **kwargs):
        id = kwargs['pk']
        user = User.objects.get(email=self.request.user)
        wishlist = WishList.objects.get(user=user, pk=id)
        wishlist.delete()
        return HttpResponseRedirect(reverse('add-to-cart'))
    
    
    # add or remove a single product from user wishlist
    def post(self, *args, **kwargs):
        id = kwargs['pk']
        quantity = int(self.request.POST['quantity'])
        user = User.objects.get(email=self.request.user)
        wishlistProduct = get_object_or_404(WishList, user=user, pk=id)
        product = wishlistProduct.product

        if quantity != 0 and product.inStock == True:
            
            wishlistProduct.quantity = quantity
            wishlistProduct.total_price = (product.price * quantity)
            wishlistProduct.save()

        elif quantity == 0 or product.inStock == False:
            wishlistProduct.delete()
            
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
        allOrders = Order.objects.filter(user=user).order_by('datatime')
        return allOrders


'''
admin
123

bdskynet75@gmail.com
Tintinbd12
'''