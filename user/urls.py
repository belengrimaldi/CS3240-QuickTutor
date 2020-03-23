from django.conf.urls import url
from django.urls import path
from . import views

#I'm not sure why but "path" makes it so that you can pass arguments and "url" doesn't

urlpatterns = [
    url(r'^$', views.Home),
    url(r'^profile/update', views.Prof),
    url(r'^profile/viewprofile', views.SeeProfile),
    url(r'^account/logout/$', views.Logout),
    url(r'^send', views.Messaging, name='send'),
    path('<str:pal_username>/', views.CorLog, name='log'),
]
