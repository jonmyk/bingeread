from django.test import SimpleTestCase
from django.urls import reverse, resolve
from bingeread.apps.core.views import view_home 

class TestCoreUrls(SimpleTestCase): 
    def test_homepage_url_resolves(self):
        url = reverse(view_home)
        self.assertEqual(resolve(url).func,view_home) 