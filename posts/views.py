from django.shortcuts import render
from .models import *
# Create your views here.

def index(request):
    categories = Category.objects.all()
    return render(request,'index.html',{'categories':categories})