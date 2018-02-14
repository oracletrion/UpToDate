from django.contrib import admin

# Register your models here.

from .models import Reddit_Post

admin.site.register(Reddit_Post)
