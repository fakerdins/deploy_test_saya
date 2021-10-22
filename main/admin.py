from django.contrib import admin
from .models import Comment, Reply, Problem, Picture

admin.site.register(Problem)
admin.site.register(Picture)
admin.site.register(Reply)
admin.site.register(Comment)