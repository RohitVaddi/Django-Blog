from django.contrib import admin
from .models import BlogComment, Contact, Post

# Register your models here.

admin.site.register(Post)
admin.site.register(Contact)
# admin.site.register(Comment)
admin.site.register(BlogComment)
