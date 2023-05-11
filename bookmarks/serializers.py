from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Bookmark
from posts.serializers import PostListSerializers

class BookmarkSerializers(ModelSerializer):
  
    post=PostListSerializers(read_only=True)
    class Meta:
        model=Bookmark
        fields=("post",)

  