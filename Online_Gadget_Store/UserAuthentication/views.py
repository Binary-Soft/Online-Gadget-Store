from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

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
            redirect_to = self.request.POST.get("next")
            login(self.request, user)
            
            if redirect_to == "" :
                return HttpResponseRedirect(reverse('home'))
            return HttpResponseRedirect(redirect_to)
            

        messages.error(self.request, "Email or Password is Incorrect.")
        return render(self.request, 'UserAuthentication/login.html')




# for user logout
def UserLogout(request):
    logout(request);
    return HttpResponseRedirect(reverse('home'))


# for user profile
class UserProfile(LoginRequiredMixin, View):
    login_url = "/user/login/"
    template_name = 'UserAuthentication/profile.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)
    
    def post(self, *args, **kwargs):
        image = self.request.FILES.get('profileimage')
        extenduser = ExtendUser.objects.get(user=self.request.user)
        
        if image is not None:
            extenduser.picture = image
            extenduser.save()
        return render(self.request, self.template_name)


# for update user information
@login_required(login_url="/user/login/")
def updateUserInfo(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phoneno = request.POST.get('phoneno')
        address = request.POST.get('address')
        extenduser = ExtendUser.objects.get(user=request.user)

        extenduser.user.first_name=name
        extenduser.user.save()
        extenduser.phone = phoneno
        extenduser.address = address
        extenduser.save()
        return HttpResponseRedirect(reverse('user-profile'))
    else:
        return HttpResponseNotFound(request)


class UserPasswordChange(UserProfile):
    template_name = 'UserAuthentication/changepassword.html'

    def post(self, *args, **kwargs):
        password = self.request.POST['password']
        confirm_password = self.request.POST['confirm_password']
        if password != confirm_password:
            messages.warning(self.request, "Password Don't Match !")
            return render(self.request, self.template_name)
        else:
            user = User.objects.get(username=self.request.user)
            user.set_password(password)
            user.save()
            update_session_auth_hash(self.request, user)  # update the current session
            messages.success(self.request, 'Your password was successfully updated!')
            return HttpResponseRedirect(reverse('user-profile'))


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
