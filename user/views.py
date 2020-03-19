from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.db import transaction
from .models import Profile, Message
from .forms import UserForm,ProfileUpdateForm, MessageForm
from django.contrib import messages

#Create your views here

@login_required
def Home(request):
    available_tutors = Profile.objects.filter(activeTutor=True)
    inbox = Message.objects.filter(receiver=request.user)
    if inbox:
        print("fart")
    template = loader.get_template('home.html')
    context = {
        'available_tutors': available_tutors,
        'inbox': inbox,
    }
    return HttpResponse(template.render(context, request))


def Send_Box(request):
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
    return render(request, 'send.html', {'form': form})

@login_required
def SeeProfile(request):
    return render(request, 'profile.html')

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

def Logout(request):
    logout(request)
    return HttpResponseRedirect('/')
