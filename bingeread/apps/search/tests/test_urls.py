from django.test import SimpleTestCase
from django.urls import reverse, resolve
from bingeread.apps.search.views import search_page


class TestSearchUrls(SimpleTestCase):

    def test_search_view_url(self):
        self.assertEquals(resolve(reverse('search_page')).func, search_page)
