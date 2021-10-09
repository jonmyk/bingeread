from django.test import TestCase 
from django.contrib.auth import get_user_model
from bingeread.apps.accounts.views import login,logout,register

User = get_user_model()


class TestModels(TestCase):

    def setUp(self):
        accountmanager1 = AccountManager.objects.create(email = 'cheesburger@fries.no',password = 'somemodels123')
        
        self.accountmanager1.save()
            
        self.account = Account.ojects.create(first_name = 'testmodel' ,last_name = 'manager 3' , email = 'mckebab@fries.no', date_joined = 3, last_login = 4, is_admin = True , is_active = False , is_staff = True, is_superuser = True)

        def test_account_create(self):
            print("test_account_create")
            qs = Account.objects.all()
            
            self.assertEquals(self.account.email,'testmodel')
            self.assertEqual(qs.count(),2)

        def test_create_super_user(self):
            
            account1 = Account.objects.create(
                AccountManager = accountmanager1,
                name = 'development'
            )

            accountmanager1 = Accountmanager.objects.create(
                email = 'kebab@fries.no',
                first_name = 'henrik',
                last_name = 'olsen',
                password = 'something'
                 
            )
            accountmanager1 = Accountmanager.objects.create(
                email = 'kebab@fries.no',
                first_name = 'henrik2',
                last_name = 'olsen2',
                password = 'something4'
                 
            ) 

            
            self.assertEquals(self.accountmanager1.create_superuser,7000) 
