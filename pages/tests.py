from django.test import TestCase

# Create your tests here.
# class LoginTestCase(TestCase):
#     def test_successful_login(self):
#         response = self.client.post('/login/', {
#             'username': 'testuser',
#             'password': 'testpass123'
#         })
#         self.assertRedirects(response, '/home/')
#
#     def test_failed_login(self):
#         response = self.client.post('/login/', {
#             'username': 'wronguser',
#             'password': 'wrongpass'
#         })
#         self.assertContains(response, 'Invalid credentials')