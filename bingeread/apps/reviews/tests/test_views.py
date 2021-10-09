from django.test import TestCase
from django.urls import reverse, resolve
from bingeread.apps.reviews.views import fetch_comments, fetch_number_of_reviews
import json
from bingeread.apps.reviews.models import Reviews
from django.contrib.auth import get_user_model

User = get_user_model()

class TestViews(TestCase):
    
    def setUp(self):

        # Need user login to bypass unauthorized and redirect issue
        self.new_user = User.objects.create(email='cheeseburger@fries.no', password='someguy123')
        self.new_user.save()

        # Review object to test fetch_comment() & fetch_number_of_reviews()
        self.review = Reviews.objects.create(uid=self.new_user, bid='test', comment='great')
        self.review.save()

        # Book ID and comment
        self.book_id = 'cheeseburger'
        self.comment = 'tasty'

        # Add_review URL
        self.add_review_url = reverse('add_review')

    def test_add_review_authorized_POST(self):

        response = self.client.force_login(self.new_user)
        data = {"book_id":self.book_id, "comment":self.comment}
        response = self.client.post(self.add_review_url, data, follow=True)
        self.assertEquals(response.status_code, 200)
    
    # Help function
    def test_fetch_comments(self):
        data = fetch_comments('test')
        for comment in data:
            print("comment:", comment)
            self.assertEquals(comment['comment'], 'great')
            
    # Help function
    def test_fetch_number_of_reviews(self):
        data = fetch_number_of_reviews('test')
        self.assertEqual(data, 1)
    
    def test_add_review_unauthorized_post(self):
        data = {"book_id":self.book_id, "comment":self.comment}
        response = self.client.post(self.add_review_url, data, follow=True)
        self.assertEquals(response.status_code, 401)
