from django.test import TestCase, Client
from django.urls import reverse, resolve
from bingeread.apps.accounts.views import login, logout, register
import json
from django.contrib.auth import get_user_model

User = get_user_model()

class TestViews(TestCase):
    
    def setUp(self):
        self.client = Client()

        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.register_url = reverse('register')

        self.new_user = User.objects.create(email='cheeseburger@fries.no', password='someguy123')
        self.new_user.save()

    def test_user_exists(self):
        user_count = User.objects.all().count()
        self.assertEquals(user_count, 1)
        self.assertNotEqual(user_count, 0)

    def test_user_password(self):
        user_qs = User.objects.filter(password="someguy123")
        user_exists = user_qs.exists() and user_qs.count() == 1
        self.assertTrue(user_exists)
        self.assertEquals(self.new_user.password, 'someguy123')

    def test_login_GET(self):
        response = self.client.get(self.login_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_POST(self):
        data = {"email":"cheeseburger@fries.no", "password":self.new_user}
        response = self.client.post(self.login_url, data, follow=True)
        redirect_path = response.request.get("PATH_INFO")
        self.assertEqual(response.status_code, 200)
    
    def test_register_POST(self):
        data = {"first_name":"James", "last_name":"Bond", "email":"Bond@007.no", "password1":"notimetodie", "password2":"notimetodie"}
        response = self.client.post(self.register_url, data, follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_register_GET(self):
        response = self.client.get(self.register_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

       
