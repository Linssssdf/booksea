from django.contrib.auth import get_user_model, user_logged_out, authenticate, login
from django.contrib.auth.forms import PasswordResetForm, AuthenticationForm
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.shortcuts import render, redirect, resolve_url
from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email

from django.http import HttpResponse

from .models import User

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'pages/index.html')
    return redirect('/home')

def home(request):
    if not request.user.is_authenticated:
        return redirect(resolve_url('login'))
    if request.user.role == User.UserRole.MANAGER:
        return render(request, 'pages/manager_home.html')
    if request.user.role == User.UserRole.CUSTOMER:
        return render(request, 'pages/customer_home.html')

    return HttpResponse('Something went wrong, this should not happen')

def signout(request):
    logout(request)
    return redirect('/')

class PasswordResetConfirmView(PasswordResetConfirmView):
    def form_valid(self, form):
        form.save()  # This resets the password
        # messages.success(self.request, 'Your password has been successfully reset. You can now log in with your new password.')
        return super().form_valid(form)

    def get_success_url(self):
        return resolve_url('login')
class PasswordResetForm(PasswordResetForm):
    def get_users(self, email):
        User = get_user_model()
        return User.objects.filter(email__iexact=email)

class PasswordResetView(PasswordResetView):
    form_class = PasswordResetForm


class UserRegistrationForm(forms.ModelForm):
     password = forms.CharField(label='Password', widget=forms.PasswordInput)
     email = forms.EmailField(label='Email')

     class Meta:
          model = User
          fields = ['username', 'email', 'password']

     def clean_password(self):
          password = self.cleaned_data.get('password')
          try:
               validate_password(password)
          except Exception as e:
               raise forms.ValidationError(e)
          return password

     def clean_email(self):
          email = self.cleaned_data.get('email')
          try:
               validate_email(email)
          except Exception as e:
               raise forms.ValidationError(e)
          if User.objects.filter(email=email).exists():
               raise forms.ValidationError('Email already in use')
          return email


def user_register(request):
     if request.method == 'POST':
          form = UserRegistrationForm(request.POST)
          if form.is_valid():
               user = form.save(commit=False)
               user.set_password(form.cleaned_data['password'])
               user.save()
               return redirect('/')
     else:
          form = UserRegistrationForm()
     return render(request, 'pages/register.html', {'form': form})


def user_login(request):
     if request.method == 'POST':
          form = AuthenticationForm(data=request.POST)
          if form.is_valid():
               username = form.cleaned_data.get('username')
               password = form.cleaned_data.get('password')
               print(username)
               user = authenticate(request, username=username, password=password)
               if user is not None:
                    login(request, user)
                    return redirect('/home')
     else:
          form = AuthenticationForm()
     return render(request, 'pages/login.html', {'form': form})

def logout(request):
    """
    Remove the authenticated user's ID from the request and flush their session
    data.
    """
    # Dispatch the signal before the user is logged out so the receivers have a
    # chance to find out *who* logged out.
    user = getattr(request, "user", None)
    if not getattr(user, "is_authenticated", True):
        user = None
    user_logged_out.send(sender=user.__class__, request=request, user=user)
    request.session.flush()
    if hasattr(request, "user"):
        from django.contrib.auth.models import AnonymousUser

        request.user = AnonymousUser()