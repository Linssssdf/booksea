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

    @property
    def is_staff(self):
        return self.role in [User.UserRole.MANAGER]

    @property
    def is_superuser(self):
        return self.role == User.UserRole.MANAGER

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

    def __str__(self):
        return self.username