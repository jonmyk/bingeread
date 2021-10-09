from django.test import TestCase, Client
from django.urls import reverse, resolve
from bingeread.apps.bookshelf.models import ListMeta, ListEntry, BookMeta
from bingeread.apps.bookshelf.views import get_lists, create_list, remove_book, add_book, delete_list, rename_list, get_books, get_list_filter
import json
from django.contrib.auth import get_user_model
import requests
import json

User = get_user_model()

class TestViews(TestCase):
    
    def setUp(self):

        # Need user login to bypass unauthorized and redirect issue
        self.new_user = User.objects.create(email='cheeseburger@fries.no', password='someguy123')
        self.new_user.save()

        # List and book info
        self.list_id = 1
        self.listname = "Novels"
        self.book_id= "_ojXNuzgHRcC"
        self.kwrd = "Pride and Prejudice"
        self.second_name = "Tortillas"

        # Meant for rename_list(), get_list_filter()
        url = 'https://www.googleapis.com/books/v1/volumes/s1gVAAAAYAAJ'
        response = requests.get(url)
        content = json.loads(response.content)
        
        self.listmeta = ListMeta.objects.create(lid= self.list_id, uid=self.new_user, name='Spaghetti', private=False)
        self.listentry = ListEntry.objects.create(lid=self.listmeta, bid="s1gVAAAAYAAJ")
        self.bookmeta = BookMeta.objects.create(id="s1gVAAAAYAAJ", selfLink=content['selfLink'],volumeInfo=content['volumeInfo'])
  
        # Client Object
        self.client = Client()

        # Url
        self.create_list_url = reverse('create_list')
        self.get_lists_url = reverse('get_lists')
        self.rename_list_url = reverse('rename_list')
        self.add_book_url = reverse('add_book')
        self.get_list_filter_url = reverse('list_filter')
        self.remove_book_url = reverse('remove_book')
        self.get_books_url = reverse('get_books')
        self.delete_list_url = reverse('delete_list')

    def test_get_create_list_POST(self):
        response = self.client.force_login(self.new_user)
        data = {"name":self.listname}
        response = self.client.post(self.create_list_url, data, follow=True)
        self.assertEquals(response.status_code, 201)

    def test_get_lists_GET(self):
        response = self.client.force_login(self.new_user)
        response = self.client.get(self.get_lists_url)
        self.assertEquals(response.status_code, 200)
    
    def test_rename_list_POST(self):
        response = self.client.force_login(self.new_user)
        data = {"name":self.second_name, "id":self.list_id}
        response = self.client.post(self.rename_list_url, data)
        self.assertEquals(response.status_code, 200)

    def test_add_book_POST(self):
        response = self.client.force_login(self.new_user)
        data = {"list_id":self.list_id, "book_id":self.book_id}
        response = self.client.post(self.add_book_url, data, follow=True)
        self.assertEquals(response.status_code, 201)

    def test_render_entry_template_POST(self):
        pass
    
    def test_get_list_filter_GET(self):
        response = self.client.force_login(self.new_user)
        data = {"kwrd":self.kwrd, "id":self.list_id}
        response = self.client.get(self.get_list_filter_url, data, follow=True)
        self.assertEquals(response.status_code, 200)

    def test_get_books_POST(self):
        response = self.client.force_login(self.new_user)
        data = {"id":self.list_id}
        response = self.client.post(self.get_books_url, data, follow=True)
        self.assertEquals(response.status_code, 200)

    def test_remove_book_POST(self):
        response = self.client.force_login(self.new_user)
        data = {"list_id":self.list_id, "book_id":"s1gVAAAAYAAJ"}
        response = self.client.post(self.remove_book_url, data, follow=True)
        self.assertEquals(response.status_code, 200)
    
    def test_delete_list_POST(self):
        response = self.client.force_login(self.new_user)
        data = {"id":self.list_id}
        response = self.client.post(self.delete_list_url, data, follow=True)
        self.assertEquals(response.status_code, 200)

    def test_response_on_AnonymousUser(self):
        response = self.client.get(reverse('bookshelf_view'))
        self.assertRedirects(response, '/accounts/login/?next=/bookshelf/')

        response = self.client.get(reverse('get_lists'))
        self.assertEquals(response.status_code, 401)

        response = self.client.post(reverse('create_list'))
        self.assertEquals(response.status_code, 401)

        response = self.client.post(reverse('rename_list'))
        self.assertEquals(response.status_code, 401)

        response = self.client.post(reverse('delete_list'))
        self.assertEquals(response.status_code, 401)

        response = self.client.get(reverse('get_books'))
        self.assertEquals(response.status_code, 401)

        response = self.client.post(reverse('add_book'))
        self.assertEquals(response.status_code, 401)

        response = self.client.post(reverse('remove_book'))
        self.assertEquals(response.status_code, 401)

    def test_missing_parameters_on_post(self):
        self.client.force_login(self.new_user)

        response = self.client.post(reverse('create_list'))
        self.assertEquals(response.status_code, 422)

        response = self.client.post(reverse('rename_list'))
        self.assertEquals(response.status_code, 422)

        response = self.client.post(reverse('delete_list'))
        self.assertEquals(response.status_code, 422)

        response = self.client.post(reverse('add_book'))
        self.assertEquals(response.status_code, 422)

        response = self.client.post(reverse('remove_book'))
        self.assertEquals(response.status_code, 422)