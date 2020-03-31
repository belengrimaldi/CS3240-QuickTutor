from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
from django.forms import ModelForm
from django import forms
import os

TIMESLOT_OPTIONS = (
    ("1","5-15 minutes"),
    ("2","15-30 minutes"),
    ("3","30 minutes-1 hour"),
    ("4", "More than 1 hour"),
)

MEETING_PLACES = (
    ("Alderman Library","Alderman Library"),
    ("Clark (Brown) Library","Clark (Brown) Library"),
    ("Clemmons Library","Clemmons Library"),
    ("Starbucks (Corner)", "Starbucks (Corner)"),
    ("Starbucks (Newcomb)", "Starbucks (Newcomb)"),
    ("Argo Tea", "Argo Tea"),
    ("Einstein Bros (Rice)", "Einstein Bros (Rice)"),
    ("15|15", "15|15"),
)

#Create your models here

class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="receiver", on_delete=models.CASCADE)
    msg_content = models.TextField(verbose_name='message content', max_length=400, blank=True)
    created_at = models.TimeField(auto_now_add=True)



class Fill_Out_Sheet(models.Model):
    has_tutor_accepted = models.BooleanField(default=False)
    has_tutor_rejected = models.BooleanField(default=True)
    sender = models.ForeignKey(User, related_name="Sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="Receiver", on_delete=models.CASCADE) 
    class_desc = models.CharField(max_length=30, blank=True)
    help_desc = models.TextField(max_length=100, blank=True)
    meeting_places = models.CharField(
        max_length = 200,
        choices = MEETING_PLACES,
        default = "15|15",
    )
    time_slot = models.CharField(
        max_length=20,
        choices = TIMESLOT_OPTIONS,
        default = '1'
        )
    def __str__(self):
        return self.class_desc

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    year = models.PositiveSmallIntegerField(blank=True, null=True)
    classes_taken = models.TextField(max_length=400, blank=True)
    help_needed = models.TextField(max_length=300, blank=True)
    image = models.ImageField(default='user/static/user/default.jpg', upload_to='profile_pics')

    active_tutor = models.BooleanField(default=False)

    def __str__(self):
            return f'{self.user.username} Profile'

    #scales down the size of images upload by users
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

@receiver(models.signals.post_delete, sender=Profile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding Profile object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)

@receiver(models.signals.pre_save, sender=Profile)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding Profile object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Profile.objects.get(pk=instance.pk).image
    except Profile.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
