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
                            year = 2021,
                            classes_taken = "Art",
                            help_needed = "CS 3240",
                            image = "default.jpg"
        )

    def test_bio(self):
        testU = Profile.user.get(bio="Hello, tutor me")
        self.assertEqual(testU.bio, "Hello, tutor me")

    def test_location(self):
        testU = Profile.user.get(location="America")
        self.assertEqual(testU.location, "America")

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
