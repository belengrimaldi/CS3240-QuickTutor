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

    def test_bio(self):
        testU = Profile.user.get(bio="Hello, tutor me")
        self.assertEqual(testU.bio, "Hello, tutor me")

    def test_location(self):
        testU = Profile.user.get(location="America")
        self.assertEqual(testU.location, "America")

    def test_bday(self):
        testU = Profile.user.get(birth_date="04/09/1999")
        self.assertEqual(testU.birth_date, "04/09/1999")

    def test_year(self):
        testU = Profile.user.get(year=2021)
        self.assertEqual(testU.year, 2021)

    def test_classes_taken(self):
        testU = Profile.user.get(classes_taken="Art")
        self.assertEqual(testU.classes_taken, "Art")

    def test_help_needed(self):
        testU = Profile.user.get(help_needed="CS 3240")
        self.assertEqual(testU.help_needed,"CS 3240")

    def test_image(self):
        testU = Profile.user.get(image="default.jpg")
        self.assertEqual(testU.image,"default.jpg")

