from django.test import TestCase
from django.db import models
from django.contrib.auth.models import User
from .models import Profile
#adding this as a test

class UserTestCase(TestCase):
    def setUp(self):
        Profile.user.create(user = User,
                            bio = "Hello, tutor me",
                            location = "America",
                            birth_date = "04/09/1999",
                            year = 2021,
                            classes_taken = "Art",
                            help_needed = "CS 3240",
                            image = "default.jpg"
        )

    def bioTest(self):
        testU = Profile.user.get(bio="Hello, tutor me")
        self.assertEqual(testU.bio, "Hello, tutor me")

    def locationTest(self):
        testU = Profile.user.get(location="America")
        self.assertEqual(testU.location, "America")

    def birth_dateTest(self):
        testU = Profile.user.get(birth_date="04/09/1999")
        self.assertEqual(testU.birth_date, "04/09/1999")

    def yearTest(self):
        testU = Profile.user.get(year=2021)
        self.assertEqual(testU.year, 2021)

    def classes_TakenTest(self):
        testU = Profile.user.get(classes_taken="Art")
        self.assertEqual(testU.classes_taken, "Art")

    def help_neededTest(self):
        testU = Profile.user.get(help_needed="CS 3240")
        self.assertEqual(testU.help_needed,"CS 3240")

    def help_neededTest(self):
        testU = Profile.user.get(image="default.jpg")
        self.assertEqual(testU.image,"default.jpg")
    
    
