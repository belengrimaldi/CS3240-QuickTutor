from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [
    url(r'^$', views.Home),
    url(r'^gethelp', views.GetHelp),
    url(r'^profile/update', views.Prof),
    url(r'^profile/viewprofile', views.SeeProfile),
    url(r'^account/logout/$', views.Logout),
    url(r'^givehelp', views.GiveHelp),
    url(r'^filloutsheet',views.filloutform),
]
