from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.db import transaction
<<<<<<< HEAD
from .models import Profile, Message
from .forms import UserForm,ProfileUpdateForm, MessageForm
=======
from .models import Profile, Fill_Out_Sheet
from .forms import UserForm, ProfileUpdateForm, FillOutSheetForm
from .models import *
>>>>>>> adding_form
from django.contrib import messages


# Create your views here


@login_required
def Home(request):
    available_tutors = Profile.objects.filter(active_tutor=True)
    template = loader.get_template('home.html')
    accepted_appoint = Fill_Out_Sheet.objects.filter(sender = request.user).filter(has_tutor_accepted=True)
    rejected_appoint = Fill_Out_Sheet.objects.filter(sender = request.user).filter(has_tutor_rejected=True)
    return render(request, 'home.html')


def filloutform(request):
    if request.method == 'POST':
        form = FillOutSheetForm(request.POST, instance=request.user)
        if form.is_valid():
            receiver_ob = User.objects.get(
                email=form.cleaned_data['recipient'])
            
            formContent = Fill_Out_Sheet(
                sender=request.user,
                receiver=receiver_ob,
                class_desc=form.cleaned_data['class_desc'],
                help_desc=form.cleaned_data['help_desc'],
                time_slot=form.cleaned_data['time_slot'],
                meeting_places=form.cleaned_data['meeting_places']
            )
            formContent.save()
            return redirect('filloutsheet.html')
    else:
        form = FillOutSheetForm()

    context = {'form': form}
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
def Messaging(request):
#   Makes the message box (the box with which to send messages)
    if request.method == "POST":
        form = MessageForm(request.POST, instance=request.user)
        if form.is_valid():
            try:
                receiver_ob = User.objects.get(email=form.cleaned_data['recipient'])
            except User.DoesNotExist:
                messages.error(request, f'The specified recipient does not exist')
                return redirect('send.html')
            msg = Message(
                sender = request.user,
                receiver = receiver_ob,
                msg_content = form.cleaned_data['msg_content'],
            )
            msg.save()
            messages.success(request, f'Your message has been sent!')
            return redirect('send.html')
    else:
        form = MessageForm()

#   Makes the list of people who you've messaged or who have messaged you
    received = Message.objects.filter(receiver=request.user)
    sent = Message.objects.filter(sender=request.user)
    pen_pals = []
    for msg in received:
        if msg.sender not in pen_pals:
            pen_pals.append(msg.sender)
    for msg in sent:
        if msg.receiver not in pen_pals:
            pen_pals.append(msg.receiver)


    context = {
        'form': form,
        'pen_pals': pen_pals,
    }


    return render(request, 'send.html', context)

def CorLog(request, pal_username):
    pen_pal = User.objects.get(username=pal_username)
    coris = []
    received = Message.objects.filter(receiver=request.user, sender=pen_pal)
    sent = Message.objects.filter(receiver=pen_pal, sender=request.user)
    for i in received:
        coris.append(i)
    for i in sent:
        coris.append(i)
    coris.sort(key=(lambda x: x.created_at), reverse=True)

    context = {
        'coris': coris,
        'pal' : pen_pal
    }
    return render(request, 'log.html', context)

@login_required
def SeeProfile(request):
    return render(request, 'profile.html')

@login_required
def GiveHelp(request):
    received = Fill_Out_Sheet.objects.filter(receiver=request.user)
    context = {'received':received,}
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
