from django.test import TestCase, Client
from django.db import models

from django.contrib.auth.models import User
from .models import Profile, Message

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


# class ActiveTutorTestCase(TestCase):
#     def setUp(self):
#         User.objects.create(email='example@example.com', first_name = 'Emma', last_name = 'Studtmann')
    
#     def test_activeTutorSetting(self):
#         my_user = User.objects.get(email='example@example.com')
#         my_profile = Profile.objects.get(user=my_user) #This will just return the one user's profile
#         my_profile.active_tutor = True


class MessageTestCase(TestCase):
    def setUp(self):

        User.objects.create(email='row@row.com', first_name = 'Rowan', last_name = 'Dakota', username='row')
        User.objects.create(email='foo@foo.com', first_name = 'Foo', last_name = 'Bar', username='foo')

    def test_Message(self):

        foo = User.objects.get(email='foo@foo.com')
        row = User.objects.get(email='row@row.com')


        msg = Message(
                sender = foo,
                receiver = row,
                msg_content = "What's up my hommie g dog?",
        )

        msg.save()
        re_msg = Message.objects.get(msg_content="What's up my hommie g dog?")
        self.assertEqual(re_msg.sender, foo)
        self.assertEqual(re_msg.receiver, row)

