from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from . models import ExtendUser
# Create your views here.


#  for user login
class UserLogin(View):
    
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return render(self.request, 'UserAuthentication/login.html')
        return HttpResponseRedirect(reverse('home'))
    
    def post(self, *args, **kwargs):
        user_email = self.request.POST['user_email']
        user_password = self.request.POST['user_password']
        user = authenticate(username=user_email, password=user_password)

        if user is not None:
            login(self.request, user)
            return HttpResponseRedirect(reverse('home'))

        messages.error(self.request, "Email or Password is Incorrect.")
        return HttpResponseRedirect(reverse('user-login'))


# for user logout
def UserLogout(request):
    logout(request);
    return HttpResponseRedirect(reverse('home'))


# for user profile
class UserProfile(LoginRequiredMixin, View):
    login_url = "/user/login/"

    def get(self, *args, **kwargs):
        return HttpResponse(str(self.request.user))


# for new user registration
class UserRegistration(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return render(self.request, 'UserAuthentication/registration.html')
        return HttpResponseRedirect(reverse('home'))
    
    def post(self, *args, **kwargs):
        name = self.request.POST['name']
        username = self.request.POST['username']
        user_email = self.request.POST['user_email']
        user_address = self.request.POST['user_address']
        user_password = self.request.POST['user_password']
        confirm_password = self.request.POST['confirm_password']

        if user_password != confirm_password:
            messages.error(self.request, "Password Don't Match !")
            return HttpResponseRedirect(reverse("user-registration"))

        elif User.objects.filter(username=username).exists():
            messages.error(self.request, 'The Username you entered has already been used. Please try another username.')
            return HttpResponseRedirect(reverse("user-registration"))
        elif User.objects.filter(email=user_email).exists():
            messages.error(self.request, 'The Email you entered has already been used. Please try another Email.')
            return HttpResponseRedirect(reverse("user-registration"))
        
        user = User.objects.create_user(username=user_email, password=confirm_password, email=username, first_name=name)
        if user is not None:
            extenduser = ExtendUser(user=user, address=user_address)
            extenduser.save()
            login(self.request, user)
            return HttpResponseRedirect(reverse("user-profile"))
        
        return render(self.request, 'UserAuthentication/registration.html')

