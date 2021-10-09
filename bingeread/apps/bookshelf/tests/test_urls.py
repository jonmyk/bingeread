from django.test import SimpleTestCase
from django.urls import reverse, resolve
from bingeread.apps.bookshelf.views import get_lists, get_books, add_book, create_list, delete_list, remove_book, bookshelf_view, rename_list, render_entry_template, get_list_filter


class TestBookshelfUrls(SimpleTestCase):

    def test_bookshelf_view_url(self):
        self.assertEquals(resolve(reverse('bookshelf_view')).func, bookshelf_view)

    def test_get_list_url(self):
        self.assertEquals(resolve(reverse('get_lists')).func, get_lists)

    def test_create_list_url(self):
        self.assertEquals(resolve(reverse('create_list')).func, create_list)
    
    def test_rename_list_url(self):
        self.assertEquals(resolve(reverse('rename_list')).func, rename_list)

    def test_delete_list_url(self):
        self.assertEquals(resolve(reverse('delete_list')).func, delete_list)

    def test_get_books_url(self):
        self.assertEquals(resolve(reverse('get_books')).func, get_books)

    def test_add_book_url(self):
        self.assertEquals(resolve(reverse('add_book')).func, add_book)

    def test_remove_book_url(self):
        self.assertEquals(resolve(reverse('remove_book')).func, remove_book)

    def test_entry_template_url(self):
        self.assertEquals(resolve(reverse('entry_template')).func, render_entry_template)
    
    def test_add_entry_url(self):
        self.assertEquals(resolve(reverse('list_filter')).func, get_list_filter)
    