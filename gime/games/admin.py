from django.contrib import admin
from django.contrib import admin
from django.contrib import admin
from .models import Game, Tag, CustomUser, Review  # Импортируйте все модели, которые используют теги и игры

admin.site.register(Game)
admin.site.register(Tag)
admin.site.register(CustomUser)
admin.site.register(Review)