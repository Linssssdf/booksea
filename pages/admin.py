from django.contrib import admin
from django.contrib.auth.models import Group

from pages.models import User

admin.site.site_header = "Library Management Admin"

# Register your models here.
admin.site.unregister(Group)
admin.site.register(User)