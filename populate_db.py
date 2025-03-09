import os
import django

from django.core.management import call_command
from faker import Faker
from faker.providers import BaseProvider
import random

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'booksea.settings')
django.setup()
from pages.models import User

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

if __name__ == '__main__':
    if "yes" not in input("This will destroy all data in the database. Are you sure? (yes/no) ").lower():
        print("Aborting...")
        exit()

    call_command('flush', interactive=False)
    print("Commencing...")

    User._default_manager.create_user('a', 'a', email="123@a.com", role=User.UserRole.CUSTOMER)
    User._default_manager.create_user('manager', 'manager', email="manager@manager.com", role=User.UserRole.MANAGER)
    create_customers()
    print("Database population completed!")