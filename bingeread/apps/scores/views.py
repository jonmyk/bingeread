from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import Avg, Count
from .models import Score


def set_score(request):
    """Create user rating for a book. Does not return the created/updated object"""
    if request.user.is_authenticated:
        try:
            obj, created = Score.objects.update_or_create(
                uid=request.user, bid=request.POST['id'],
                defaults={'score': request.POST['score']},
            )
            status = 201 if created else 200
        except MultiValueDictKeyError:
            status = 422
    else:
        status = 401
    return HttpResponse(status=status)


def remove_score(request):
    """Remove user's rating of a book"""
    if request.user.is_authenticated:
        status = 200
        try:
            Score.objects.get(
                uid=request.user, bid=request.POST['id']
            ).delete()
        except MultiValueDictKeyError:
            status = 422
        except ObjectDoesNotExist:
            status = 404
    else:
        status = 401
    return HttpResponse(status=status)


def get_score_user(request):
    """Fetches a user's rating for a book"""
    if request.user.is_authenticated:
        status = 200
        try:
            score = Score.objects.get(
                uid=request.user, bid=request.GET['id'],
            ).score
        except MultiValueDictKeyError:
            status = 422
        except ObjectDoesNotExist:
            # NOTE: Could have used 404, but did't want to handled it as an error
            status = 204
    else:
        status = 401

    data = {'score': score} if (status == 200) else {}
    return JsonResponse(data, status=status)


def get_score_global(request):
    """Fetches the global rating (avg, count) for a book"""
    data = Score.objects.filter(
        bid=request.GET.get('id', None)
    ).aggregate(avg=Avg('score'), count=Count('bid'))

    if data['count'] == 0:
        data['avg'] = 0

    return JsonResponse(data)
