from rest_framework.serializers import ModelSerializer
from .models import PostLike
from posts.serializers import TinyPostSerializers

class PostLikeSerializers(ModelSerializer):
    post= TinyPostSerializers()
   
    class Meta:
        model=PostLike
        fields=("post",)

       

