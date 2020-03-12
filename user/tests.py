from django.test import TestCase
from django.db import models
from django.contrib.auth.models import User
from .models import Profile

class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(email='example@example.com', first_name = 'Emma', last_name = 'Studtmann')


    def test_UserExists_Test(self):
        self.assertNotEquals(User.objects.get(email='example@example.com'), None)
    
    def test_profile(self):
        my_user = User.objects.get(email='example@example.com')
        my_profile = Profile.objects.get(user=my_user) #This will just return the one user's profile
        #profile = Profile.objects.filter(bio='Tutor me') This will return a list of all of the profiles which have this bio
        #profile = Profile.objects.filter(bio='Tutor me').filter(location = 'Roanoke') This will return a list of all of the profiles which have this bio
        self.assertNotEquals(my_profile, None)

