from django.shortcuts import render
from django.http import HttpResponse, JsonResponse 
from django.core import serializers
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist, ValidationError
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Lower
from django.utils.datastructures import MultiValueDictKeyError
from django.forms.models import model_to_dict

import requests
import json
from django.contrib.auth.models import auth

from .models import *


@login_required(login_url='login')
def bookshelf_view(request):
    """Fetches the bookshelf page. Redirects if not authenticated"""
    return render(request, 'bookshelf.html')

def get_lists(request):
    """Returns all lists of a user in alphabetical order"""
    if request.user.is_authenticated:
        model = ListMeta.objects.filter(uid=request.user).order_by(Lower('name'))
        response = serializers.serialize('json', model)
        return JsonResponse(response, status=200, safe=False) 
    else:
        return JsonResponse({}, status=401)

def create_list(request):
    """Creates and returns a new list"""
    if request.user.is_authenticated:
        try:
            name = request.POST['name']
            obj, created = ListMeta.objects.get_or_create(uid=request.user, name=name)
        except Exception as e:
            return exception_handler(e)
        response = serializers.serialize('json', [obj])[1:-1]
        if created:
            return JsonResponse(response, status=201, safe=False)
        else:
            return JsonResponse(response, status=409, safe=False)
    else:
        return JsonResponse({}, status=401)

def rename_list(request):
    """Updates the name of a list and returns the updated record"""
    if request.user.is_authenticated:
        try:
            name = request.POST['name']
            id = request.POST['id']
            model = ListMeta.objects.get(lid=id, uid=request.user)
            model.name = name
            model.save()
        except Exception as e:
            return exception_handler(e)
        response = serializers.serialize('json', [model])[1:-1]
        return JsonResponse(response, status=200, safe=False)
    else:
        return JsonResponse({}, status=401)

def delete_list(request):
    """Removes the list and all its entires from the database"""
    status = 200
    if request.user.is_authenticated:
        try:
            id = request.POST['id']
            ListMeta.objects.get(uid=request.user, lid=id).delete()
        except MultiValueDictKeyError:
            status = 422        
        except MultipleObjectsReturned:
            status=500
        except ObjectDoesNotExist:
            status=404
    else:
        status=401
    return HttpResponse(status=status) 

def get_books(request):
    """Fetches all the books from a list"""
    if request.user.is_authenticated:
        try:
            List = ListEntry.objects.filter(lid=ListMeta.objects.get(
                uid=request.user, lid=request.POST['id']))
            content = [model_to_dict(BookMeta.objects.get(id=book.bid)) for book in List]
        except Exception as e:
            return exception_handler(e)
        return JsonResponse(json.dumps(content), status=200, safe=False)
    else:
        return JsonResponse({}, status=401)

def add_book(request):
    """Adds a book to a list. Returns the created object"""
    if request.user.is_authenticated:
        try:
            list_id = request.POST['list_id']
            book_id = request.POST['book_id']
            list_obj = ListMeta.objects.get(uid=request.user, lid=list_id)
            obj, created = ListEntry.objects.get_or_create(lid=list_obj, bid=book_id)
        except Exception as e:
            return exception_handler(e)

        response = serializers.serialize('json', [obj])[1:-1]
        if created:
            status, msg = create_book(book_id)
            if status == 200 or status == 201:
                return JsonResponse(response, status=201, safe=False)
            else:
                return JsonResponse({}, status=status)
        else:
            return JsonResponse(response, status=409, safe=False)
    else:
        return JsonResponse({}, status=401)

def remove_book(request):
    """Removes a book from a list"""
    status = 200
    if request.user.is_authenticated:
        try:
            ListEntry.objects.get(
                bid=request.POST['book_id'],
                lid=ListMeta.objects.get(
                    uid=request.user, lid=request.POST['list_id']), 
            ).delete()
        except MultiValueDictKeyError:
            status = 422
        except MultipleObjectsReturned:
            status = 500
        except ObjectDoesNotExist:
            status = 404
    else:
        status = 401
    return HttpResponse(status=status)

def exception_handler(e):
    """Exception handler for methods that returns json responses"""
    if e.__class__ == MultiValueDictKeyError:
        return JsonResponse({}, status=422) # Missing parameter
    elif e.__class__ == MultipleObjectsReturned:
        return JsonResponse({}, status=500) # Database conflict (duplicate records)
    elif e.__class__ == ObjectDoesNotExist:
        return JsonResponse({}, status=404) # Record not found
    elif e.__class__ == ValidationError:
        return JsonResponse(e.message_dict, status=400, safe=False) # Validation error
    else:
        return JsonResponse({}, status=400) # Unknown error

def create_book(id):
    """
    Store a book's metadata locally to speedup list entry lookup time
    Returns tuple: (status, message)
    """
    if BookMeta.objects.filter(id=id).exists():
       return (200, 'Ok')

    url = 'https://www.googleapis.com/books/v1/volumes/' + id
    response = requests.get(url)    
    if response.status_code == 200:
        content = json.loads(response.content)
        try:
            record = BookMeta(
                id=id,
                selfLink=content['selfLink'],
                volumeInfo=content['volumeInfo']
            )
            record.save()
        except Exception as e:
            return (400, e)
        return (201, 'Created')
    return (response.status_code, response.text)

def render_entry_template(request):
    """Renders the list entry template"""
    try:
        book = json.loads(request.POST['book'])
    except:
        return HttpResponse(status=400)
    return render(request, 'list-entry.html', {'book': book})

def get_list_filter(request):
    """Fetches all the books from a list"""
    if request.user.is_authenticated:
        try:
            List = ListEntry.objects.filter(lid=ListMeta.objects.get(
                uid=request.user, lid=request.GET['id']))
            book_pool = [model_to_dict(BookMeta.objects.get(id=book.bid)) for book in List]
            keywords = request.GET['kwrd']
            result = [book for book in book_pool if BookMeta.objects.filter(
                id=book['id'], volumeInfo__icontains=keywords
                ).count() > 0]
        except Exception as e:
            return exception_handler(e)
        return JsonResponse(json.dumps(result), status=200, safe=False)
    else:
        return JsonResponse({}, status=401)
 
def fetch_lists(uid):
    """Returns all lists of a user. It is used by other apps on the server-side."""
    return ListMeta.objects.filter(uid=uid).values()
