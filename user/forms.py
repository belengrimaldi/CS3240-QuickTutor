from django.shortcuts import redirect, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from user.models import Profile, Message
from django import forms


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'location', 'year', 'classes_taken', 'help_needed', 'image', 'active_tutor')

class MessageForm(forms.ModelForm):
    recipient = forms.EmailField(label="Recipient's email", max_length=200)
    class Meta:
        model = Message
        fields = ('recipient', 'msg_content')
