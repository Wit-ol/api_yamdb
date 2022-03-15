from django.contrib import admin

from .models import User


@admin.register(User)
class AuthorAdmin(admin.ModelAdmin):
    fields = ('username', 'email', 'password',
              'first_name', 'last_name', 'bio', 'role', 'is_superuser')
