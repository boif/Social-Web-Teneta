from django.contrib import admin
from News.models import *

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)