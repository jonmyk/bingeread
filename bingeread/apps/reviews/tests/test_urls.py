
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from bingeread.apps.reviews.views import add_review

class TestReviewstUrls(SimpleTestCase):

    def test_add_review_url(self):
        self.assertEquals(resolve(reverse('add_review')).func, add_review) 

        