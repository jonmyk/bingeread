from django.shortcuts import render
from django.http import HttpResponse
from django.forms.models import model_to_dict
from bingeread.apps.reviews.views import fetch_comments, fetch_number_of_reviews
from bingeread.apps.reviews.models import Reviews
from bingeread.apps.bookshelf.models import BookMeta
from bingeread.apps.bookshelf.views import fetch_lists

import json
import requests

from bingeread.apps.scores.views import *
from bingeread.apps.reviews.views import *

def bookpage(request, id):
	"""Render the book page"""
	
	number_of_reviews = fetch_number_of_reviews(id)
	comments = fetch_comments(id)
	lists = fetch_lists(request.user) if request.user.is_authenticated else []

	# Improves performance by fetching book info from the database instead of the api when possible
	try:
		content = model_to_dict(BookMeta.objects.get(id=id))
		return render(request, 'book.html', {'content':content, 'comments':comments, 'reviews':number_of_reviews, 'lists':lists})
	except Exception:
		url = 'https://www.googleapis.com/books/v1/volumes/' + id
		resp = requests.get(url)
		if resp.status_code == 200:
			content = json.loads(resp.content)
			return render(request, 'book.html', {'content':content, 'comments':comments, 'reviews':number_of_reviews, 'lists':lists})
		elif resp.status_code ==  404:
			return HttpResponse({}, status=404)
		else:
			return HttpResponse({}, status=503)
