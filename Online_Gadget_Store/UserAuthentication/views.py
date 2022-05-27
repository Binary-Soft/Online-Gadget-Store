from django.shortcuts import render, HttpResponseRedirect
from django.views import View
from django.contrib.auth import authenticate, login, logout

# Create your views here.


#  for user login
class UserLogin(View):
    
    def get(self, *args, **kwargs):
        return render(self.request, 'UserAuthentication/login.html')
    
    def post(self, *args, **kwargs):
        user_email = self.request.POST['user_email']
        user_password = self.request.POST['user_password']
        user = authenticate(username=user_email, password=user_password)
        if user is not None:
            login(self.request, user)
            print(user)
            return HttpResponseRedirect('/')
        
        return render(self.request, 'base.html')


def UserLogout(request):
    logout(request);
    return HttpResponseRedirect('/')



class UserRegistration(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'base.html')
    
    def post(self, *args, **kwargs):
        user_email = self.request.POST['user_email']
        user_password = self.request.POST['user_password']
        user_password = self.request.POST['user_password']
        user = authenticate(username=user_email, password=user_password)

        if user is not None:
            login(self.request, user)
            return HttpResponseRedirect('')
        
        return render(self.request, 'base.html')

