from django.forms.models import model_to_dict
from django.shortcuts import render
import random

from bingeread.apps.bookshelf.views import ListMeta, ListEntry, BookMeta


def frontpage(request):
    return render(request,'templates/home/home.html')

def view_home(request):
    response = {}
    try:
        response['todays_content'] = [
            model_to_dict(BookMeta.objects.get(id=book.bid)) 
            for book in 
            ListEntry.objects.filter(lid=ListMeta.objects.get(lid=1))
        ]
    except Exception:
        print("List 'Featured Today' not fond")
    
    try:
        response['classics_content'] = [
            model_to_dict(BookMeta.objects.get(id=book.bid)) 
            for book in 
            ListEntry.objects.filter(lid=ListMeta.objects.get(lid=2))
        ]
    except Exception:
        print("List 'Classics' not fond")
    
    try:
        response['fantasy_content'] = [
            model_to_dict(BookMeta.objects.get(id=book.bid)) 
            for book in 
            ListEntry.objects.filter(lid=ListMeta.objects.get(lid=3))
        ]
    except Exception:
        print("List 'Fantasy' not fond")
    
    try:
        response['editors_content'] = [
            model_to_dict(BookMeta.objects.get(id=book.bid)) 
            for book in 
            ListEntry.objects.filter(lid=ListMeta.objects.get(lid=4))
        ]
    except Exception:
        print("List 'Editor's Picks' not fond")

    return render(request, 'home.html', response)
