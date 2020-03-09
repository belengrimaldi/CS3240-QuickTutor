from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Home),
    url(r'^profile/update', views.Prof),
    url(r'^profile/viewprofile', views.SeeProfile),
    url(r'^account/logout/$', views.Logout),
]
