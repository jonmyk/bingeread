from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account


class AccountAdmin(UserAdmin):
	exclude = ('username', )
	list_display = ('first_name', 'last_name', 'email', 'date_joined', 'last_login', 'is_admin', 'is_staff')
	search_fields = ('first_name', 'last_name', 'email')
	readonly_fields = ('date_joined', 'last_login')
	filter_horizontal = ()
	list_filter = ()
	fieldsets = (
		('Personal info', {'fields': ('first_name', 'last_name', 'email', 'password')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}))
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('first_name', 'last_name', 'email', 'password1', 'password2'),}),)
	ordering = ['email']


admin.site.register(Account, AccountAdmin)