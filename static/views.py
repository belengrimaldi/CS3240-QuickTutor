from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template import loader
# Create your views here.

def about(request):
    return render(request, 'static/about.html')
