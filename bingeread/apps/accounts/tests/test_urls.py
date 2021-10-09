from django.test import SimpleTestCase
from django.urls import reverse, resolve
from bingeread.apps.accounts.views import login, logout, register



class TestUrls(SimpleTestCase):

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func,login)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func,logout)


    def test_register_url_resolves(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func,register)
