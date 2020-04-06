from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template import loader
from django.conf.urls import url
from django.urls import path
import stripe

# Create your views here.

def about(request):
    return render(request, 'static/about.html')

def FAQ(request):
    return render(request, 'static/FAQ.html')