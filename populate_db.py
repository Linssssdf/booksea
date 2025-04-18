import os
from datetime import timedelta
from django.utils import timezone
import django

from django.core.management import call_command
from faker import Faker
from faker.providers import BaseProvider
import random

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'booksea.settings')
django.setup()
from pages.models import User, Book, LibraryEvent, Announcement


class GlasgowLocationProvider(BaseProvider):
    # Google tells me this is roughly within glasgow city
    def glasgow_latitude(self):
        return round(random.uniform(55.8, 55.9), 6)

    def glasgow_longitude(self):
        return round(random.uniform(-4.3, -4.2), 6)

fake = Faker()
fake.add_provider(GlasgowLocationProvider)

def create_users(num_users=10):
    for _ in range(num_users):
        username = fake.user_name()
        email = fake.email()
        password = fake.password()
        display_name = fake.name()
        birthday = fake.date_of_birth(minimum_age=18, maximum_age=30)
        college = fake.company()
        role = User.UserRole.CUSTOMER
        balance = round(random.uniform(5.0, 50.0), 2)
        User.objects.create_user(username=username, email=email, password=password, display_name=display_name, birthday=birthday, balance=balance, college=college, role=role)
    print(f"Created {num_users} customers")


def create_fake_books():
    """Create some fake book data if not already created."""
    fake_books = [
        {'title': 'Java Programming', 'category': 'Programming', 'index': 'P1', 'img': '/img/java.jpg',
         'is_available': True, 'rental_price': 10.99},
        {'title': 'Python', 'category': 'Programming', 'index': 'P2', 'img': '/img/python.jpg', 'is_available': True,
         'rental_price': 12.50},
        {'title': 'Data Science', 'category': 'Data Science', 'index': 'D1', 'img': '/img/data_science.jpg',
         'is_available': True, 'rental_price': 15.00},
        {'title': 'Machine Learning', 'category': 'AI & ML', 'index': 'M1', 'img': '/img/machine_learning.jpg',
         'is_available': False, 'rental_price': 18.75},
        {'title': 'To Kill a Mockingbird', 'category': 'Novel', 'index': 'N1', 'img': '/img/to_kill_a_mockingbird.jpg',
         'is_available': True, 'rental_price': 8.99},
        {'title': '1984', 'category': 'Novel', 'index': 'N2', 'img': '/img/1984.jpg', 'is_available': False,
         'rental_price': 9.50},
        {'title': 'Pride and Prejudice', 'category': 'Novel', 'index': 'N3', 'img': '/img/pride_and_prejudice.jpg',
         'is_available': True, 'rental_price': 10.25},
        {'title': 'Sapiens: A Brief History of Humankind', 'category': 'History', 'index': 'H1',
         'img': '/img/sapiens.jpg', 'is_available': True, 'rental_price': 14.00},
        {'title': 'Guns, Germs, and Steel', 'category': 'History', 'index': 'H2', 'img': '/img/guns_germs_steel.jpg',
         'is_available': False, 'rental_price': 13.99},
        {'title': 'The Art of War', 'category': 'History', 'index': 'H3', 'img': '/img/art_of_war.jpg',
         'is_available': True, 'rental_price': 11.75},
        {'title': 'The Story of Art', 'category': 'Art', 'index': 'A1', 'img': '/img/story_of_art.jpg',
         'is_available': True, 'rental_price': 17.99},
        {'title': 'Ways of Seeing', 'category': 'Art', 'index': 'A2', 'img': '/img/ways_of_seeing.jpg',
         'is_available': True, 'rental_price': 12.75},
        {'title': 'The Elements of Graphic Design', 'category': 'Art', 'index': 'A3',
         'img': '/img/elements_of_graphic_design.jpg', 'is_available': True, 'rental_price': 14.50},
    ]

    for book in fake_books:
        borrow_date = timezone.now() if not book['is_available'] else None
        due_date = timezone.now() + timedelta(days=7) if not book['is_available'] else None

        Book.objects.get_or_create(
            title=book['title'],
            category=book['category'],
            index=book['index'],
            img=book['img'],
            borrow_date=borrow_date,
            due_date=due_date,
            is_available=book['is_available'],
            rental_price=book['rental_price']
        )

def create_fake_events():
    events = [
        {
            "title": "New Book Wall is Now Open",
            "description": "After some careful preparation, the newly upgraded smart book recommendation wall has been launched. It allows for AI book recommendation: you can input your reading preferences, and the system will provide you with a personalized recommendation list of books. The inaugural batch includes 500+ award-winning books from 2025.",
            "date": timezone.make_aware(timezone.datetime(2025, 1, 1, 0)),
            "event_type": "Book Club",
            "location": "First Floor Reception"
        },
        {
            "title": "Literature and Society Book Club",
            "description": "We invite all book lovers to join our discussion on 'Literature and Society.' This session will focus on the significance of George Orwell's 1984 in today's world. Free refreshments and **limited edition bookmarks** will be available.",
            "date": timezone.make_aware(timezone.datetime(2025, 2, 13, 19)),
            "event_type": "Seminar",
            "poster": "/img/reading_meeting.jpg",
            "location": "Seminar Room, Third Floor"
        },
        {
            "title": "Children's Story Workshop Upgrade",
            "description": "Join our new 'Story + Handmade' immersive experience! On February 17, we’ll feature a Harry Potter-themed event with **3D book making and role-playing games.",
            "date": timezone.make_aware(timezone.datetime(2025, 2, 17, 10)),
            "event_type": "Workshop",
            "poster": "/img/children_activity.jpg",
            "location": "Children's Reading World"
        },
        {
            "title": "24-Hour Study Area Now Open",
            "description": "Our brand-new **Smart Study Space** offers:\n✦ Private study booths with wireless charging\n✦ Self-service coffee and snacks\n✦ Silent zone & video learning room\n✦ Early bird membership reservations now open.",
            "date": timezone.make_aware(timezone.datetime(2025, 3, 1, 13)),
            "event_type": "Other",
            "poster": "/img/open_space.jpg",
            "location": "Study Hall"
        },
        {
            "title": "'Friends of the Library' Membership",
            "description": "Exclusive benefits include:\n✦ Priority access to new book loans\n✦ Reserved seating at reading clubs\n✦ Annual customized book list service\n✦ Discounts at partner bookstores",
            "date": timezone.make_aware(timezone.datetime(2025, 3, 3, 2)),
            "event_type": "Other",
            "location": "Main Library Hall"
        }
    ]

    for event in events:
        LibraryEvent.objects.get_or_create(
            title=event['title'],
            description=event['description'],
            date=event['date'],
            event_type=event['event_type'],
            poster=event.get('poster', None),
            location=event['location']
        )
def create_announcement():
    announcements = [
        {"title": "New Features Launched", "content": "Self-service borrowing and returning book functions. You can now borrow and return books without admin intervention!"},
    ]

    for ann in announcements:
        Announcement.objects.get_or_create(title=ann["title"], content=ann["content"])

if __name__ == '__main__':
    if "yes" not in input("This will destroy all data in the database. Are you sure? (yes/no) ").lower():
        print("Aborting...")
        exit()

    call_command('flush', interactive=False)
    print("Commencing...")

    User._default_manager.create_user('a', 'a12345678', email="123@a.com", role=User.UserRole.CUSTOMER)
    User._default_manager.create_user('manager', 'manager123', email="manager@manager.com", role=User.UserRole.MANAGER)
    create_users()
    create_fake_books()
    create_fake_events()
    create_announcement()
    print("Database population completed!")