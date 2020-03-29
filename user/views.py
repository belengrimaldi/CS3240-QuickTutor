from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.db import transaction
from .models import Profile, Fill_Out_Sheet
from .forms import UserForm, ProfileUpdateForm, FillOutSheetForm
from .models import *
from django.contrib import messages

# Create your views here


@login_required
def Home(request):
    return render(request, 'home.html')


def filloutform(request):
    if request.method == 'POST':
        form = FillOutSheetForm(request.POST, instance=request.user)
        if form.is_valid():
            receiver_ob = User.objects.get(email=form.cleaned_data['recipient'])
            formContent = Fill_Out_Sheet(
                sender=request.user,
                reciever=receiver_ob,
                class_desc=form.cleaned_data['class_desc'],
                help_desc=form.cleaned_data['help_desc'],
                time_slot=form.cleaned_data['time_slot'],
                meeting_places=form.cleaned_data['meeting_places'],
            )
            formContent.save()
            return redirect('filloutsheet.html')
    else:
        form = FillOutSheetForm()

    received = Fill_Out_Sheet.objects.filter(receiver=request.user)
    sent = Fill_Out_Sheet.objects.filter(sender=request.user)
    pen_pals = []
    for msg in received:
        if msg.sender not in pen_pals:
            pen_pals.append(msg.sender)
    for msg in sent:
        if msg.receiver not in pen_pals:
            pen_pals.append(msg.receiver)

    context = {'form': form}
    return render(request, 'filloutsheet.html', context)


@login_required
def corLogForFOS(request, pal_username):
    pen_pal = User.objects.get(username=pal_username)
    coris = []
    received = Fill_Out_Sheet.objects.filter(
        receiver=request.user, sender=pen_pal)
    sent = Fill_Out_Sheet.objects.filter(receiver=pen_pal, sender=request.user)
    for i in recieved:
        coris.append(i)
    for i in sent:
        coris.append(i)
    # could put a sort here by time created, but really unnecessary for fill out form i think
    context = {
        'coris': coris,
        'pal': pen_pal,
    }
    return render(request, 'filloutsheet.html', context)


@login_required
def GetHelp(request):
    available_tutors = Profile.objects.filter(active_tutor=True)
    template = loader.get_template('gethelp.html')
    context = {
        'available_tutors': available_tutors,
    }
    return render(request, 'gethelp.html', context)


@login_required
def SeeProfile(request):
    return render(request, 'profile.html')


@login_required
def GiveHelp(request):
    available_tutees = Fill_Out_Sheet.objects.filter(
        tutor_name=request.user.first_name)
    template = loader.get_template('gethelp.html')
    context = {
        'available_tutees': available_tutees,
    }
    return render(request, 'givehelp.html', context)

# @login_required
# def Tutee(request):
#     return render(request, 'tutee.html')


@login_required
def Prof(request):
    if request.method == 'POST':
        u_form = UserForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('update_profile.html')
    else:
        u_form = UserForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'update_profile.html', context)


"""
@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect('/')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'home/update_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
"""


def Logout(request):
    logout(request)
    return HttpResponseRedirect('/')
