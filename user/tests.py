from django.test import TestCase, Client
from django.db import models

from django.contrib.auth.models import User
from .models import Profile, Message

class UserTestCase(TestCase):
      def test_stupid(self):
          self.assertEqual(1,1)
#     def setUp(self):

#         User.objects.create(email='example@example.com', first_name = 'Emma', last_name = 'Studtmann')

#     def test_UserExists_Test(self):
#         self.assertNotEquals(User.objects.get(email='example@example.com'), None)
    
#     def test_profile(self):
#         my_user = User.objects.get(email='example@example.com')
#         my_profile = Profile.objects.get(user=my_user) #This will just return the one user's profile
#         #profile = Profile.objects.filter(bio='Tutor me') This will return a list of all of the profiles which have this bio
#         #profile = Profile.objects.filter(bio='Tutor me').filter(location = 'Roanoke') This will return a list of all of the profiles which have this bio
#         self.assertNotEquals(my_profile, None)


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
        User.objects.create(email='poo@poo.com', first_name = 'Poo', last_name = 'Poo', username='poo')

    def test_Message(self):

         foo = User.objects.get(email='foo@foo.com')
         row = User.objects.get(email='row@row.com')
         poo = User.objects.get(email='poo@poo.com')

         msg = Message(
                 sender = foo,
                 receiver = row,
                 msg_content = "What's up my hommie g dog?",
         )

         msg.save()
         re_msg = Message.objects.get(msg_content="What's up my hommie g dog?")
         self.assertEqual(re_msg.sender, foo)
         self.assertEqual(re_msg.receiver, row)
         self.assertNotEquals(re_msg.sender, poo)
         self.assertNotEquals(re_msg.sender, None)


