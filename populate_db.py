import os
import django

from django.core.management import call_command
from faker import Faker
from faker.providers import BaseProvider
import random

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'booksea.settings')
django.setup()
from pages.models import User, Book


class GlasgowLocationProvider(BaseProvider):
    # Google tells me this is roughly within glasgow city
    def glasgow_latitude(self):
        return round(random.uniform(55.8, 55.9), 6)

    def glasgow_longitude(self):
        return round(random.uniform(-4.3, -4.2), 6)

fake = Faker()
fake.add_provider(GlasgowLocationProvider)

def create_customers(num_users=10):
    for _ in range(num_users):
        username = fake.user_name()
        email = fake.email()
        password = fake.password()
        display_name = fake.name()
        role = User.UserRole.CUSTOMER
        User.objects.create_user(username=username, email=email, password=password, display_name=display_name, role=role)
    print(f"Created {num_users} customers")

def create_fake_books():
    """Create some fake book data if not already created."""
    fake_books = [
        {'title': 'Java Programming', 'category': 'Programming', 'index': 'J', 'is_available': True, 'rental_price': 10.99},
        {'title': 'Python', 'category': 'Programming', 'index': 'P', 'is_available': True, 'rental_price': 12.50},
        {'title': 'Data Science', 'category': 'Data Science', 'index': 'D', 'is_available': True, 'rental_price': 15.00},
        {'title': 'Machine Learning', 'category': 'AI & ML', 'index': 'M', 'is_available': True, 'rental_price': 18.75},
    ]
    for book in fake_books:
        Book.objects.get_or_create(
            title=book['title'],
            category=book['category'],
            index=book['index'],
            is_available=book['is_available'],
            rental_price=book['rental_price']
        )

if __name__ == '__main__':
    if "yes" not in input("This will destroy all data in the database. Are you sure? (yes/no) ").lower():
        print("Aborting...")
        exit()

    call_command('flush', interactive=False)
    print("Commencing...")

    User._default_manager.create_user('a', 'a12345678', email="123@a.com", role=User.UserRole.CUSTOMER)
    User._default_manager.create_user('manager', 'manager123', email="manager@manager.com", role=User.UserRole.MANAGER)
    create_customers()
    create_fake_books()
    print("Database population completed!")