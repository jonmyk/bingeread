from django.test import TestCase
import json
import requests
from django.contrib.auth import get_user_model
from bingeread.apps.bookshelf.views import ListMeta, ListEntry, BookMeta


User = get_user_model()

class TestModels(TestCase):

    def setUp(self):

        new_user = User.objects.create(email='cheeseburger@fries.no', password='someguy123')
        new_user.save()

        url = 'https://www.googleapis.com/books/v1/volumes/s1gVAAAAYAAJ'
        response = requests.get(url)
        self.content = json.loads(response.content)

        self.listmeta = ListMeta.objects.create(lid=70, uid=new_user, name='Testlist', private=False)
        self.listentry = ListEntry.objects.create(lid=self.listmeta, bid='s1gVAAAAYAAJ')
        self.bookmeta = BookMeta.objects.create(id='s1gVAAAAYAAJ', selfLink=self.content['selfLink'],volumeInfo=self.content['volumeInfo'])

    def test_listmeta_creation(self):
        self.assertEquals(self.listmeta.name, 'Testlist')
    
    def test_list_entry_creation(self):
        self.assertEquals(self.listentry.bid, 's1gVAAAAYAAJ')
    
    def test_bookmeta_creation(self):
        self.assertEquals(self.bookmeta.id, 's1gVAAAAYAAJ')
        self.assertEquals(self.bookmeta.selfLink, self.content['selfLink'])
        self.assertEquals(self.bookmeta.volumeInfo, self.content['volumeInfo'])
        