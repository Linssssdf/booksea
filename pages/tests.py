from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Book, Support, Announcement
from datetime import datetime, timedelta
from django.utils import timezone

User = get_user_model()

class LibraryViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='test1234', balance=50.0)
        self.manager = User.objects.create_user(username='admin', email='manager@example.com', password='admin123', role=User.UserRole.MANAGER)
        self.book = Book.objects.create(title='Test Book', category='Test', index='T1', rental_price=10.0, is_available=True)

    def test_index_view(self):
        response = self.client.get(reverse('index'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/index.html')

    def test_home_view_redirect_log_out(self):
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('login'))

    def test_home_view_for_customer(self):
        self.client.login(username='testuser', password='test1234')
        response = self.client.get(reverse('home'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_home_view_for_manager(self):
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('manager_home'))

    def test_add_book_as_manager(self):
        self.client.login(username='admin', password='admin123')
        response = self.client.post(reverse('add_book'), {
            'title': 'New Book',
            'category': 'Science',
            'index': '5678',
            'rental_price': '15.0',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Book.objects.filter(title='New Book').exists())

    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'NewPassword123'
        })
        self.assertEqual(User.objects.count(), 3)
        self.assertRedirects(response, reverse('login'))

    def test_user_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'test1234'
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/customer_home.html')

    def test_borrow_book_with_sufficient_balance(self):
        self.client.login(username='testuser', password='test1234')
        response = self.client.post(reverse('borrow_book', args=[self.book.id]))
        self.book.refresh_from_db()
        self.user.refresh_from_db()
        self.assertFalse(self.book.is_available)
        self.assertEqual(self.book.borrower, self.user)
        self.assertEqual(self.user.balance, 40.0)
        self.assertRedirects(response, reverse('book_detail'))

    def test_return_book_no_late_fee(self):
        self.client.login(username='testuser', password='test1234')
        self.book.is_available = False
        self.book.borrower = self.user
        self.book.due_date = timezone.now() + timedelta(days=1)
        self.book.save()
        response = self.client.post(reverse('return_book', args=[self.book.id]))
        self.book.refresh_from_db()
        self.assertTrue(self.book.is_available)
        self.assertEqual(self.book.borrower, None)
        self.assertRedirects(response, reverse('order'))

    def test_account_setting_update(self):
        self.client.login(username='testuser', password='test1234')
        response = self.client.post(reverse('account_setting'), {
            'name': 'Updated Name',
            'birthday': '1990-01-01',
            'college': 'Test College',
            'email': 'updated@example.com'
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.display_name, 'Updated Name')
        self.assertEqual(self.user.email, 'updated@example.com')
        self.assertRedirects(response, reverse('account_setting'))

    def test_balance_top_up(self):
        self.client.login(username='testuser', password='test1234')
        response = self.client.post(reverse('balance'), {'amount': '20.0'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.balance, 70.0)
        self.assertRedirects(response, reverse('balance'))

    def test_support_message_submission(self):
        self.client.login(username='testuser', password='test1234')
        response = self.client.post(reverse('support'), {'support_message': 'Need help'})
        self.assertEqual(Support.objects.count(), 1)
        self.assertRedirects(response, reverse('support'))

    def test_news_view(self):
        response = self.client.get(reverse('news'))
        self.assertEqual(response.status_code, 200)

    def test_announcement_view(self):
        Announcement.objects.create(title='Important Update', content='Library closed on Sunday')
        response = self.client.get(reverse('announcement'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Important Update')
