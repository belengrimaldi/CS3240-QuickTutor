from django.shortcuts import redirect, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from user.models import Profile
from django import forms
from user.models import Fill_Out_Sheet


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio','location', 'year', 'classes_taken', 'help_needed', 'image', 'active_tutor')

class FillOutSheetForm(forms.ModelForm):
    recipient = forms.EmailField(label="Recipient's email",max_length=200)
    class Meta:
        model = Fill_Out_Sheet
        fields = ('recipient','class_desc','help_desc','time_slot', 'meeting_places',)