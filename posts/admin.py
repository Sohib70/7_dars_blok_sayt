from django.contrib import admin
from django.template.defaultfilters import title

from .models import Category,Comment,Contact,User,Saved,News
# Register your models here.

class NewaAdmin(admin.ModelAdmin):
    list_display = ['category','title','user','created_at']
    list_filter = ['category','user']
    search_fields = ['category__name','title']

admin.site.register(News,NewaAdmin)

admin.site.register(Category)