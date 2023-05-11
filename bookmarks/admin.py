from django.contrib import admin
from .models import Bookmark

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_daisply=("id", "post")
    list_daisply_link=("id", "post")
