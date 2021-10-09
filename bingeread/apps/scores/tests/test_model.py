from django.db.models import constraints
from django.test import TestCase
from django.contrib.auth import get_user_model 
from bingeread.apps.scores.models import Score


User = get_user_model()
class Testmodels(TestCase):
    def setUp(self):
        new_user = User.objects.create(email='taco@fries.no', password='someboy423')
        new_user_2 = User.objects.create(email='taco2@fries.no', password='someboy4235')
        new_user_3 = User.objects.create(email='kebab@.no',password='little123')

        new_user.save()
        new_user_2.save()
        new_user_3.save()

        self.score = Score.objects.create(uid = new_user,bid = 'Testlist', score=False)
        self.score = Score.objects.create(uid = new_user_2,bid = 'Testlist', score=False)
        self.score = Score.objects.create(uid = new_user_3,bid='Testlist',score =False)
      
    def test_scorecreation(self):
        self.assertEquals(self.score.bid, 'Testlist')

    def test_scorecreation_2(self):
        self.assertEquals(self.score.bid, 'Testlist')

    def test_scorecreation_3(self):
        self.assertEquals(self.score.bid, 'Testlist')

    def test_bid(self):
        max_length = self.score._meta.get_field('bid').max_length
        self.assertEquals(max_length, 16) 

    def test_sid(self):
        field_label = self.score._meta.get_field('sid').verbose_name
        self.assertEquals(field_label,'sid')

    def test_uid(self):
        field_label = self.score._meta.get_field('uid').verbose_name
        self.assertEquals(field_label,'uid')  

      