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
<<<<<<< HEAD
    url(r'^filloutsheet',views.filloutform),
    path('payment', views.payment, name='payment'),
    path('payment/success', views.success, name='success')
=======
    path('charge/', views.charge, name='charge'),
>>>>>>> 91bc0bcbdee5411f2d7ca57a84a2e7057c71d87b
]
