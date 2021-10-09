from bingeread.apps.scores.views import remove_score, set_score,get_score_user,get_score_global
from django.test import SimpleTestCase
from django.urls import reverse, resolve

class TestScoreUrls(SimpleTestCase):
    def test_set_url_resolves(self):
        url = reverse('set_score')
        self.assertEqual(resolve(url).func,set_score)

    def test_remove_url_resolves(self):
        url = reverse(remove_score)
        self.assertEqual(resolve(url).func,remove_score)

    def test_get_score_user_url_resolves(self):
        url = reverse(get_score_user)
        self.assertEqual(resolve(url).func,get_score_user)

    def test_user_url_resolves(self):
        url = reverse( get_score_global)
        self.assertEqual(resolve(url).func,get_score_global)   
