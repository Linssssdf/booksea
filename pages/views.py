from datetime import datetime, timedelta
from django.utils import timezone

from django.contrib import messages
from django.contrib.auth import get_user_model, user_logged_out, authenticate, login
from django.contrib.auth.forms import PasswordResetForm, AuthenticationForm
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.http import HttpResponse
from .models import User, Book, LibraryEvent


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'pages/index.html')
    return redirect('/home')

def home(request):
    if not request.user.is_authenticated:
        return redirect(resolve_url('login'))
    if request.user.role == User.UserRole.MANAGER:
        return redirect('manager_home')
    if request.user.role == User.UserRole.CUSTOMER:
        return render(request, 'pages/customer_home.html')

    return HttpResponse('Something went wrong, this should not happen')

def signout(request):
    logout(request)
    return redirect('/')

class PasswordResetConfirmView(PasswordResetConfirmView):
    def form_valid(self, form):
        form.save()  # This resets the password
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
               return redirect('/accounts/login/')
     else:
          form = UserRegistrationForm()
     return render(request, 'pages/register.html', {'form': form})


def user_login(request):
     if request.method == 'POST':
          form = AuthenticationForm(request, data=request.POST)
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

def support(request):
    return render(request, "pages/support.html")

def news(request):
    # Show latest events first
    events = LibraryEvent.objects.order_by('-date')
    return render(request, "pages/news.html", {'events': events})

def account_setting(request):
    if request.method == "POST":
        user = request.user
        user.display_name = request.POST.get("name", user.display_name)
        user.birthday = request.POST.get("birthday", user.birthday)
        user.college = request.POST.get("college", user.college)
        user.email = request.POST.get("email", user.email)
        user.save()
        return redirect('account_setting')
    return render(request, "pages/account_setting.html")

def balance(request):
    if request.method == "POST":
        user = request.user
        try:
            amount = request.POST.get("amount")
            amount = float(amount) if amount else 0.0
            if user.balance is None:
                user.balance = 0.0
            if amount > 0.0:
                user.balance += amount
                user.save()
        except ValueError:
            print("balance error")

        return redirect('balance')

    return render(request, "pages/balance.html")

def order(request):
    borrowed_books = Book.objects.filter(is_available=False, borrower=request.user)
    return render(request, "pages/order.html", {"borrowed_books": borrowed_books})

def book_detail(request):
    books = Book.objects.all()
    return render(request, "pages/book_detail.html", {'books': books})

def borrow_book(request, book_id):
    """Allow users to borrow a book if they have enough balance."""
    if request.method == "POST":
        book = get_object_or_404(Book, id=book_id)
        user = request.user  # Get the currently logged-in user

        if book.is_available:
            rental_price = book.rental_price  # Get book rental price

            if user.balance is not None and user.balance >= rental_price:
                user.balance -= rental_price
                user.save()
                # Update book status
                book.is_available = False
                book.borrow_date = datetime.now()
                book.due_date = datetime.now() + timedelta(days=7)
                book.borrower = user
                book.save()

                messages.success(request, f"You have successfully borrowed {book.title}.")
                return redirect('book_detail')
            else:
                messages.error(request, "Insufficient balance. Please top up your account.")
                return redirect('book_detail')

    return redirect('book_detail')

def return_book(request, book_id):
    """Allow users to return a borrowed book with an overdue fee if applicable."""
    if request.method == "POST":
        book = get_object_or_404(Book, id=book_id)
        user = request.user

        if not book.is_available:
            overdue_fee = 5.00  # £5 late fee
            is_overdue = book.due_date and timezone.now() > book.due_date

            if is_overdue:
                if user.balance is not None and user.balance >= overdue_fee:
                    user.balance -= overdue_fee  # Deduct late fee
                    user.save()
                    messages.warning(request, f"Book returned late! £5 has been deducted as a late fee.")
                else:
                    messages.error(request, "You do not have enough balance to cover the £5 late fee. Please top up.")
                    return redirect('order')  # Prevent return if fee can't be paid

            book.is_available = True
            book.borrow_date = None
            book.due_date = None
            book.borrower = None
            book.save()

            messages.success(request, f"You have successfully returned {book.title}.")

    return redirect('order')

def manager_home(request):
    borrowed_books = Book.objects.filter(
        is_available=False
    ).select_related('borrower')

    for book in borrowed_books:
        if book.due_date:
            book.is_overdue = book.due_date < timezone.now()

    stats = {
        'total_books': Book.objects.count(),
        'available_books': Book.objects.filter(is_available=True).count(),
        'overdue_books': Book.objects.filter(
            is_overdue=book.is_overdue,
            is_available=False
        ).count()
    }

    return render(request, 'pages/manager_home.html', {
        'borrowed_books': borrowed_books,
        'stats': stats
    })

def add_book(request):
    if request.method == 'POST':
        try:
            Book.objects.create(
                title=request.POST['title'],
                category=request.POST['category'],
                index=request.POST['index'],
                rental_price=request.POST['rental_price'],
                is_available=True,
            )
            return redirect('manager_home')
        except Exception as e:
            print(f"Error while adding book: {e}")

    return render(request, 'pages/manager_home.html')