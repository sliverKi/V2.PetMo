from django.contrib import admin
from .models import PostLike

@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display=("id", "user", "post")

