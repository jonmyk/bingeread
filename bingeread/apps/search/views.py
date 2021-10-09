from django.shortcuts import render
from django.http import HttpResponse

import json
import requests

from bingeread.apps.scores.views import *
from bingeread.apps.bookshelf.views import fetch_lists

BASE_URL = 'https://www.googleapis.com/books/v1/volumes?q='
BOOKS_PER_PAGE = 40

def search_page(request):
    if len(request.GET):
        return search_filter(request)
    else:
        return render(request, 'search.html')


def search_filter(request):
    """
    Calls the API using a query with the given terms. 
    Return the response, the query, and the user's lists
    """
    q = request.GET.get('q', '')
    title = request.GET.get('title', '')
    authors = request.GET.get('authors', '')
    page = int(request.GET.get('page', '1'))
    langcode = request.GET.get('langcode', '')
        
    # Search keywords
    search = q.replace(' ', '+')
    search += '+intitle:"'+title.replace(' ', '+')+'"' if title else ''
    search += '+inauthor:"'+authors.replace(' ', '+')+'"' if authors else ''

    # Search terms
    terms = '&printType=books'
    terms += '&maxResults='+str(BOOKS_PER_PAGE)
    terms += '&startIndex='+str(BOOKS_PER_PAGE*(page-1))
    terms += '&langRestrict='+langcode if langcode else ''
    # BUG: The api will sometimes return a different 'totalItems' value even if the 'startIndex' term is the only thing changed

    # API call
    url = BASE_URL + search + terms
    resp = requests.get(url)
    print("response status code with fake request:", resp.status_code)
    if resp.status_code != 200:
        return HttpResponse(status=resp.status_code)
    content = json.loads(resp.content)

    result = {
        'content': content,
        'itemsPerPage': BOOKS_PER_PAGE,
        'query': {
            'q': q,
            'title': title,
            'authors': authors,
            'langcode': langcode,
            'page': page
        },
        'lists': fetch_lists(request.user) if request.user.is_authenticated else []
    }

    return render(request, 'search.html', result)