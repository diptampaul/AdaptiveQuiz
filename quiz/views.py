from django.shortcuts import render
from .models import Quiz

# Create your views here.

def home(request):
    return render(request, 'index.htm', {})