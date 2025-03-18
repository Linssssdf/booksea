from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models


# Create your models here.
class UserManager(BaseUserManager):
    """
    Custom user manager for `User`
    """

    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The username cannot be empty')
        if not password:
            raise ValueError('The password must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('role', User.UserRole.MANAGER)
        return self.create_user(username, email, password, **extra_fields)

    def get_by_natural_key(self, username: str):
        return self.get(username=username)

class User(AbstractBaseUser):
    """
    A user of the system

    Attributes:
        username (str): The username of the user
        password (str): The password of the user
        email (str): The email of the user
        display_name (str): The name displayed for the user
        role (UserRole): The role of the user, defaults to `UserRole.CUSTOMER`
        balance (float): The balance of the user
    """
    objects = UserManager()

    USERNAME_FIELD = 'username'

    class UserRole(models.IntegerChoices):
        CUSTOMER = 1, 'Customer'
        MANAGER = 10, 'Manager'

    username = models.CharField(max_length=20, unique=True)
    display_name = models.CharField(max_length=30)
    role = models.IntegerField(
        choices=UserRole.choices, default=UserRole.CUSTOMER)
    email = models.CharField(max_length=50, unique=True)
    birthday = models.DateField(null=True, blank=True)
    college = models.CharField(max_length=100, blank=True)
    balance = models.FloatField(null=True)

    @property
    def is_staff(self):
        return self.role in [User.UserRole.MANAGER]

    @property
    def is_superuser(self):
        return self.role == User.UserRole.MANAGER

    def __str__(self):
        return self.username

class Book(models.Model):
    """
    Represents a book in the library system.

    Attributes:
        title (str): The title of the book.
        category (str): The category/genre of the book.
        index (str): The unique index identifier for the book.
        is_available (bool): Whether the book is currently available for borrowing.
        rental_price (float): The rental price of the book.
        borrow_date (datetime): The date the book was borrowed.
        due_date (datetime): The due date for returning the book.
        borrower (User): The user who borrowed the book.
        is_overdue (bool): Whether the book is overdue.
    """
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    index = models.CharField(max_length=50, unique=True)
    is_available = models.BooleanField(default=True)
    img = models.CharField(max_length=255)
    rental_price = models.FloatField(null=True)
    borrow_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    is_overdue = models.BooleanField(default=False)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="borrowed_books")

    def __str__(self):
        return f"{self.title} ({self.index})"

class LibraryEvent(models.Model):
    """
    Represents an event organized by the library.

    Attributes:
        title (str): The title of the event.
        description (str): A detailed description of the event.
        date (datetime): The scheduled date and time of the event.
        event_type (str): The category/type of the event (e.g., book club, author talk).
        location (str): The venue where the event takes place.
        poster(img):The path of image
    """
    EVENT_TYPES = [
        ("Book Club", "Book Club"),
        ("Author Talk", "Author Talk"),
        ("Workshop", "Workshop"),
        ("Seminar", "Seminar"),
        ("Other", "Other"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES, default="Other")
    location = models.CharField(max_length=255,default='Main Library')
    poster = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.date.strftime('%Y-%m-%d %H:%M')}"

class Inventory(models.Model):
    """
    Represents the inventory system for books in the library.

    Attributes:
        book (Book): The book associated with this inventory entry.
        quantity (int): Number of copies available in stock.
    """
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name="inventory")
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Inventory for {self.book.title} - {self.quantity} copies"

