from django.contrib import admin
from news.models import Post, Like, Comment

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
