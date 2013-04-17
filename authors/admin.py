from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from authors.models import Author

admin.site.register(Author, UserAdmin)
admin.site.unregister(Group)
