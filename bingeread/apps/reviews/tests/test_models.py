

from django.test import TestCase
from django.contrib.auth import get_user_model
from bingeread.apps.reviews.models import Reviews

User = get_user_model()

class TestModels(TestCase):

    def setUp(self):

        new_user = User.objects.create(email='cheeseburger@fries.no', password='someguy123')
        new_user.save()

        self.review = Reviews.objects.create(uid=new_user, bid='sunnyday', comment='lovely')

    def test_review_creation(self):
        self.assertEquals(self.review.bid, 'sunnyday')
        self.assertEquals(self.review.comment, 'lovely')
