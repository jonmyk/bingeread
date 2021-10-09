from django.test import TestCase, Client
from django.urls import reverse, resolve
from bingeread.apps.scores.views import *
from bingeread.apps.scores.models import Score
import json
from django.contrib.auth import get_user_model

User = get_user_model()

class TestViews(TestCase):

    def setUp(self):
        self.new_user = User.objects.create(email='cheeseburger@fries.no', password='123')
        self.new_user.save()

        self.book_id = 's1gVAAAAYAAJ'
        self.score = 7
        self.new_score = 10

        self.score_obj = Score.objects.create(uid=self.new_user, bid=self.book_id, score=self.score)

        self.client = Client()
        self.csrf_client = Client(enforce_csrf_checks=True)

        self.set_score_url = reverse('set_score')
        self.remove_score_url = reverse('remove_score')
        self.get_score_user_url = reverse('get_score_user')
        self.get_score_global_url = reverse('get_score_global')

    def test_set_score_POST(self):
        """unauthorized user should not be able to post a score"""
        response = self.client.force_login(self.new_user)
        data={'id':'audietron','score':2}
        response=self.client.post(self.set_score_url, data)
        self.assertEquals(response.status_code,201)


    def test_get_score_user_GET(self):
        response = self.client.force_login(self.new_user)
        data={'id':self.book_id}
        response =self.client.get(self.get_score_user_url, data)

        self.assertEquals(response.status_code,200)
        self.assertEquals(response.json(),{'score': self.score}) 
        self.assertEquals(self.score_obj.bid, self.book_id)

    def test_get_score_global(self):
        data={'id':self.book_id}
        response =self.client.get(self.get_score_global_url, data)
        self.assertEquals(response.status_code,200)
        self.assertEquals(response.json(),{'avg': self.score, 'count': 1})

    def test_remove_score(self):
        response = self.client.force_login(self.new_user)
        data={'id':self.book_id}
        response =self.client.post(self.remove_score_url, data)
        self.assertEquals(response.status_code,200)

    def test_special_cases(self):

        # Set Score
        response = self.client.force_login(self.new_user)
        data={}
        response=self.client.post(self.set_score_url, data)
        self.assertEquals(response.status_code,422)

        # Remove score fake ID
        response = self.client.force_login(self.new_user)
        data={'id':'fakeid'}
        response =self.client.post(self.remove_score_url, data)
        self.assertEquals(response.status_code,404)

        # Remove score no data
        response = self.client.force_login(self.new_user)
        data={}
        response =self.client.post(self.remove_score_url, data)
        self.assertEquals(response.status_code,422)

        # Get score user with fake ID
        response = self.client.force_login(self.new_user)
        data={'id':'fakeid'}
        response =self.client.get(self.get_score_user_url, data)
        self.assertEquals(response.status_code,204)

        # Get score user with do nata
        response = self.client.force_login(self.new_user)
        data={}
        response =self.client.get(self.get_score_user_url, data)
        self.assertEquals(response.status_code,422)


    def test_Anonymouse_user(self):
       
        # Test unauthorized set score
        data = {'id':self.book_id,'score':self.new_score}
        response = self.client.post(self.set_score_url, data, follow=True)
        self.assertEquals(response.status_code, 401)

        # Test unauthorized remove score
        data={'id': self.book_id}
        response =self.client.post(self.remove_score_url, data)
        self.assertEquals(response.status_code,401)

        # Test unauthorized get score user
        data={'id':self.book_id}
        response =self.client.get(self.get_score_user_url, data)
        self.assertEquals(response.status_code,401)

        



