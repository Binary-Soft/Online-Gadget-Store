from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView

from . models import Category, Product

# Create your views here.


class HomeView(TemplateView):
    template_name = "productstemplate/home.html"

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex['categories'] = Category.objects.all().order_by('category_name')
        contex['products'] = Product.objects.all().order_by('-datatime')
        return contex


class SpecificCategoryAllProducts(TemplateView):
    template_name = "productstemplate/products.html"

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        products = Product.objects.filter(category=category).all().order_by('-datatime')
        contex['category'] = category
        contex['specificallproducts'] = products
        return contex