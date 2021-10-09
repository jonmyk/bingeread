from django.test import SimpleTestCase
from django.urls import reverse, resolve
from bingeread.apps.bookpage.views import bookpage 


class Testbookpage_listUrls(SimpleTestCase):

    def setUp(self):
        self.book_id = 's1gVAAAAYAAJ'
    
    def test_bookshelf_view_url(self):
        self.assertEquals(resolve(reverse('bookpage', args=[self.book_id])).func, bookpage)
