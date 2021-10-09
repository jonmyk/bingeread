from django.test import TestCase, Client
from django.urls import reverse


class TestViews(TestCase):
    
    def setUp(self):

        # List and book info
        self.title = "Pride and Prejudice"
        self.authors = "Jane Austen"

        # Client Object
        self.client = Client()

        # Url
        self.search_page_url = reverse('search_page')

    # Works fine
    def test_search_page_GET(self):
   
        response = self.client.get(self.search_page_url, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search.html')

    # Works fine
    def test_search_filter(self):

        data = {"title":self.title, "authors":self.authors}

        response = self.client.get(self.search_page_url, data, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search.html')
    
    # This should not return 200!!!
    def test_search_filter_invalid_data(self):
        data = {"title":'jdnwkjldncv13r@æ3e9', "authors":'lsfvanvanåæø-'}
        response = self.client.get(self.search_page_url, data, follow=True)
        self.assertEquals(response.status_code, 200)