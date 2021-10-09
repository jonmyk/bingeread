from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils import timezone

from .models import *



def add_review(request):
    """Adds new review. If the user have already added a review, the review is updated"""
    book_id = request.POST['book_id']
    comment = request.POST['comment']
    date = timezone.now()

    if request.user.is_authenticated and request.method == 'POST':

        if request.POST['comment']:
            obj, created = Reviews.objects.get_or_create(uid=request.user, bid=book_id)
            obj = Reviews.objects.get(uid=request.user, bid=book_id)
            obj.comment = comment
            obj.date = date
            obj.save()

        if request.META.get('HTTP_REFERER') == None and Reviews.objects.filter(uid=request.user, bid=book_id).exists():
            return JsonResponse({}, status=200, safe=False)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return JsonResponse({}, status=401, safe=False)


def fetch_comments(book_id):

    review_objs = Reviews.objects.filter(bid=book_id)
    ordered_reviews=review_objs.order_by('date')
    comments, users, data, date = [],[],[],[]

    if ordered_reviews:
        for review in ordered_reviews:
            comments.append(review.comment)
            users.append(review.uid)
            date.append(str(review.date))
        if comments and users:
            comments = [x.strip(' ') for x in comments]
            
            for user, comment, date in zip(users,comments,date):
                data.append({'user': user, 'comment': comment, 'date':date})   

            for d in data:
                print(d)
    return data


def fetch_number_of_reviews(book_id):
    data = Reviews.objects.filter(bid=book_id).count()
    return data

