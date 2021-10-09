from django.urls import path
from . import views

urlpatterns = [
    path('', views.bookshelf_view, name="bookshelf_view"),
    path('lists/', views.get_lists, name="get_lists"),
    path('create/', views.create_list, name="create_list"),
    path('rename/', views.rename_list, name="rename_list"),
    path('delete/', views.delete_list, name="delete_list"),
    path('books/', views.get_books, name="get_books"),
    path('add/', views.add_book, name="add_book"),
    path('remove/', views.remove_book, name="remove_book"),
    path('entry/', views.render_entry_template, name="entry_template"),
    path('filter/', views.get_list_filter, name="list_filter"),
]