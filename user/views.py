from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.db import transaction
from .models import Profile, Fill_Out_Sheet, Message
from .forms import UserForm, ProfileUpdateForm, FillOutSheetForm, MessageForm, ChatForm, ActiveTutorForm
from django.contrib import messages
from django.conf import settings
import stripe

# Create your views here

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def Home(request):
    available_tutors = Profile.objects.filter(active_tutor=True)
    template = loader.get_template('home.html')
    return render(request, 'home.html')


def filloutform(request):
    if request.method == 'POST':
        form = FillOutSheetForm(request.POST, instance=request.user)
        if form.is_valid():
            receiver_ob = User.objects.get(
                email=form.cleaned_data['recipient'])
            
            formContent = Fill_Out_Sheet(
                has_tutor_accepted = False,
                has_tutor_rejected = False,
                no_response = True,
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
    key = settings.STRIPE_PUBLISHABLE_KEY
    #awaiting = Fill_Out_Sheet.objects.filter(sender = request.user).filter(no_response = True)
    awaiting = Fill_Out_Sheet.objects.filter(sender = request.user).filter(no_response = True)
    accepted = Fill_Out_Sheet.objects.filter(sender = request.user).filter(no_response = False).filter(has_tutor_accepted=True)
    rejected = Fill_Out_Sheet.objects.filter(sender = request.user).filter(no_response = False).filter(has_tutor_rejected=True)
    available_tutors = Profile.objects.filter(active_tutor=True)
    template = loader.get_template('gethelp.html')
    
    classes_taken_query = request.GET.get('classes_taken')
    year_query = request.GET.get('year')

    if classes_taken_query != '' and classes_taken_query is not None:
        available_tutors = available_tutors.filter(classes_taken__icontains=classes_taken_query)
    
    if year_query != '' and year_query is not None:
        available_tutors = available_tutors.filter(year__icontains=year_query)

    context = {
        'available_tutors': available_tutors,
        'awaiting':awaiting,
        'accepted':accepted,
        'rejected':rejected,
        'key':key,
    }

    return render(request, 'gethelp.html', context)

# Stripe class
# class PayView(TemplateView):
#     template_name = 'gethelp.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['key'] = settings.STRIPE_PUBLISHABLE_KEY
#         return context


@login_required
def charge(request):
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=2000,
            currency='usd',
            description='A Django Charge',
            source=request.POST['stripeToken']
        )
        return render(request, 'charge.html')


@login_required
def Messaging(request):
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
        'pen_pals': pen_pals,
    }


    return render(request, 'send.html', context)

@login_required
def CorLog(request, pal_username):
    pen_pal = User.objects.get(username=pal_username)
    coris = []

    #Make send box at bottom of screen
    if request.method == "POST":
        form = ChatForm(request.POST, instance=request.user)
        if form.is_valid():
            msg = Message(
                sender = request.user,
                receiver = pen_pal,
                msg_content = form.cleaned_data['msg_content'],
            )
            msg.save()

    form = ChatForm()

    #Make corrispondence list that's displayed
    # received = Message.objects.filter(receiver=request.user, sender=pen_pal)
    # sent = Message.objects.filter(receiver=pen_pal, sender=request.user)
    # for i in received:
    #     coris.append(i)
    # for i in sent:
    #     coris.append(i)
    # coris.sort(key=(lambda x: x.created_at), reverse=True)

    allMsg = Message.objects.filter(receiver=pen_pal, sender=request.user) | Message.objects.filter(receiver=request.user, sender=pen_pal)
    allMsgOrdered = allMsg.order_by('-created_at')
    for i in allMsgOrdered:
        coris.append(i)
    
    coris.sort(key=(lambda x: x.created_at), reverse=True)

    context = {
        'coris': coris,
        'pal' : pen_pal,
        'form' : form,
    }
    return render(request, 'log.html', context)

@login_required
def SeeProfile(request):
    return render(request, 'profile.html')

@login_required
def GiveHelp(request):
    if request.method == 'POST':
        at_form = ActiveTutorForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if at_form.is_valid():
            at_form.save()
            return redirect('givehelp.html')
    else:
        at_form = ActiveTutorForm(instance=request.user)
    tut = request.user.profile
    received = Fill_Out_Sheet.objects.filter(receiver=request.user)
    context = {'received':received,'at_form': at_form, 'tut':tut}
    return render(request, 'givehelp.html', context)

@login_required
def AcceptTutee(request, form_id):
    sheet = Fill_Out_Sheet.objects.get(pk = form_id)
    sheet.no_response = False
    sheet.has_tutor_accepted = True
    sheet.has_tutor_rejected = False
    sheet.save()
    context = {'sheet':sheet,}
    return render(request, 'givehelp.html', context)

@login_required
def RejectTutee(request, form_id):
    sheet = Fill_Out_Sheet.objects.get(pk = form_id)
    sheet.no_response = False
    sheet.has_tutor_rejected = True
    sheet.has_tutor_accepted = False
    sheet.save()
    context = {'sheet':sheet,}
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
