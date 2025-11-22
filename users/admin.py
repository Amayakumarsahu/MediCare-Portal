from django.contrib import admin
from .models import CustomUser
from .models import Category, BlogPost


admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(BlogPost)
