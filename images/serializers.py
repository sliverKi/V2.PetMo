from rest_framework.serializers import ModelSerializer
from .models import Image


class ImageSerializers(ModelSerializer):
    class Meta:
        model = Image
        fields = ("img_path",)