from rest_framework.serializers import ModelSerializer
from rest_framework import status
from .models import Category


class BoardSerializers(ModelSerializer):
    class Meta:
        model = Category
        fields = ("categoryType",)
        read_only=False