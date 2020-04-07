from django.conf.urls import url
from django.urls import path
from . import views
from django.urls import path

#I'm not sure why but "path" makes it so that you can pass arguments and "url" doesn't

urlpatterns = [
    url(r'^$', views.Home),
    url(r'^gethelp', views.GetHelp),
    url(r'^filloutsheet', views.filloutform),
    url(r'^profile/update', views.Prof),
    url(r'^profile/viewprofile', views.SeeProfile),
    url(r'^account/logout/$', views.Logout),
    url(r'^send', views.Messaging, name='send'),
    path('<str:pal_username>/send/', views.CorLog, name='log'),
    path('<int:form_id>/givehelp/accept/', views.AcceptTutee, name='accepttutee'),
    path('<int:form_id>/givehelp/reject/', views.RejectTutee, name='rejecttutee'),
    url(r'^givehelp', views.GiveHelp),
    path('<str:pal_username>/gethelp/', views.PayView.as_view(), name='payment'), # stripe
]
