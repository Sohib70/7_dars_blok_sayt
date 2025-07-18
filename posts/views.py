from django.shortcuts import render
from django.template.defaulttags import comment
from django.contrib import messages

from .models import *
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    categories = Category.objects.all()
    first_news = []
    for category in categories:
        category_first_post = News.objects.filter(category=category).order_by('-id').first()
        if category_first_post is not None:
            first_news.append(category_first_post)
    if len(first_news) < 4:
        news = News.objects.all()
        first_news.extend(news[len(news)-4:len(news)-len(first_news)])
    news = News.objects.all().order_by('-created_at')
    return render(request,'index.html',{'categories':categories,'first_news':first_news})
@login_required(login_url='login')
def category(request,pk):
    category = Category.objects.get(id=pk)
    news = News.objects.filter(category=category).order_by('-id')
    return render(request,'category-01.html',{'news':news,'category':category})

def new_detail(request,pk):
    post = News.objects.get(id=pk)
    comments = Comment.objects.all().order_by('-id')[:3]
    if request.method == 'POST':
        comment = request.POST['msg']
        Comment.objects.create(
            news = post,
            pos_text = comment,
            user = request.user
        )
        messages.info(request,'Commit qoldirildi')

    return render(request,'blog-detail-01.html',{'post':post,'comments':comments})



