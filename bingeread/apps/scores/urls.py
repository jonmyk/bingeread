from django.urls import path
from . import views

urlpatterns = [
    path('add', views.set_score, name='set_score'),
    path('remove', views.remove_score, name='remove_score'),
    path('user', views.get_score_user, name='get_score_user'),
    path('global', views.get_score_global, name='get_score_global'),
]