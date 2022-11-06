from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from Accounts.forms import LoginForm, UserCreateForm
from django.contrib.auth import authenticate, login, logout


class StartView(View):
    def get(self, request):
        return render(request, 'base.html')


class RegistrationView(SuccessMessageMixin, View):
    def get(self, request):
        form = UserCreateForm()
        return render(request, 'registration.html', {'form': form})

    def post(self, request):
        form = UserCreateForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data['password']
            un = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            u = User()
            u.username = un
            u.first_name = first_name
            u.last_name = last_name
            u.email = email
            u.set_password(password)
            u.save()
            return redirect('login')
        return render(request, 'registration.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                url = request.GET.get('next', "index")
                login(request, user)
        return redirect(url)


class Logout(View):
    def get(self, request):
        username = request.user.username
        logout(request)
        return render(request, 'base.html')

