from django.contrib import admin
from .models import *

class ListMetaAdmin(admin.ModelAdmin):
	list_display = ('lid', 'uid', 'name', 'private')
	search_fields = ('uid', 'name')
	list_filter = ('private',)
	ordering = ('uid',)

class ListEntryAdmin(admin.ModelAdmin):
	list_display = ('lid', 'bid')
	search_fields = ('lid__name', 'bid')
	list_filter = ('lid__name',)
	ordering = ('lid',)

class BookMetaAdmin(admin.ModelAdmin):
	list_display = ('id', 'selfLink')
	ordering = ('id',)

admin.site.register(ListMeta, ListMetaAdmin)
admin.site.register(ListEntry, ListEntryAdmin)
admin.site.register(BookMeta, BookMetaAdmin)