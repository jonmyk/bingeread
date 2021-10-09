from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class TestViews(TestCase):
    
    def setUp(self):
        self.book_id = 's1gVAAAAYAAJ'
        self.invalid_book_id = '9789382563792'

        # Client Object
        self.client = Client()

        # Url
        self.bookpage_url = reverse('bookpage', args=[self.book_id])
        self.bookpage_url_invalid_id = reverse('bookpage', args=[self.invalid_book_id])
    
    def test_bookpage_GET(self):
        data = {"id":self.book_id}
        response = self.client.get(self.bookpage_url, data, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'book.html')
    
    def test_bookpage_invalid_id(self):
        data = {"id": self.invalid_book_id}
        response = self.client.get(self.bookpage_url_invalid_id, data, follow=True)
        # Response will be either not found or service is unavailable
        self.assertIn(response.status_code, {503, 404})
        

        
