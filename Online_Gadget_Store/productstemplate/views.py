from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.


class HomeView(TemplateView):
    template_name = "productstemplate/home.html"

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        return contex