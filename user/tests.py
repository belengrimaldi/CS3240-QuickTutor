from django.test import TestCase
from django.db import models
from django.contrib.auth.models import User
from .models import Profile

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
