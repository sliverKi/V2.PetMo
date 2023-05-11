from django.contrib import admin
from .models import Post, Comment
from images.models import Image

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=("id","user","post","content",)
    list_display_links=("id","user","post","content",)
    search_fields=("user",)


class ImageInline(admin.StackedInline):
    model=Image  

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines=(ImageInline,)
    list_display=("id","categoryType", "user", "content","createdDate")
    list_display_links=("id","user", "content")
    search_fields=("categoryType","boardAnimalTypes", "user",)
