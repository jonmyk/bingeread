from django.contrib import admin
from .models import *


class ScoreAdmin(admin.ModelAdmin):
	readonly_fields = ['sid']
	list_display = ('sid', 'uid', 'bid', 'score')
	list_filter = ('uid', 'bid')

admin.site.register(Score, ScoreAdmin)
