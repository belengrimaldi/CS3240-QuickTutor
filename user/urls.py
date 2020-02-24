from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Home),
    url(r'^profile/update', views.Profile),
    url(r'^profile/tutor', views.Tutor),
    url(r'^profile/tutee', views.Tutee),
    url(r'^account/logout/$', views.Logout),
]
