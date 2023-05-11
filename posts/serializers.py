from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.pagination import CursorPagination
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework.response import Response
from rest_framework import status


from users.serializers import TinyUserSerializers
from .models import Post,Comment
from images.models import Image
from images.serializers import ImageSerializers
from categories.models import Category
from categories.serializers import BoardSerializers
from pets.models import Pet
from pets.serializers import PetsSerializers
from likes.models import PostLike
from bookmarks.models import Bookmark

import sys

from django.db import transaction
sys.setrecursionlimit(100000)


class CommentSerializers(ModelSerializer):
    class Meta:
        model=Comment
        fields=( 
            "pk",
            "parent_comment",
            "post",  
            "user",
            "content",
            "createdDate",
            "updatedDate"
        ) 

class ReplySerializers(ModelSerializer):
    children=serializers.SerializerMethodField()
    
    class Meta:
        model=Comment
        fields=(
            "id",
            "parent_comment",
            "post",  
            "user",
            "content",
            "createdDate",
            "updatedDate",
            "children"
        )

    def get_children(self, obj):
        children=Comment.objects.filter(parent_comment=obj.id).order_by('createdDate')
        if not children.exists():
            return None
        serializer=ReplySerializers(children, many=True,)
        return serializer.data
    
    def get_coments_count(self, obj):
        return obj.coments_count
    


class TinyPostSerializers(ModelSerializer):#좋아요 기능에서 이용
    Image=ImageSerializers(many=True, read_only=True, required=False)
    class Meta:
        model=Post
        fields=(
            "pk",
            "content",
            "Image",
            "createdDate",
            "likeCount"#게시글 좋아요 수 
            )
class PostSerializers(ModelSerializer):#댓글 없음.
    categoryType=BoardSerializers(many=True, read_only=True)
    boardAnimalTypes=PetsSerializers(many=True, read_only=True)
    user=TinyUserSerializers(read_only=True)
    Image=ImageSerializers(many=True, read_only=True, required=False)
    likeCheck=serializers.SerializerMethodField()#현재 사용자가 게시글을 좋아요 했는지를 여부를 나타냄
    
    class Meta:
        model=Post
        fields=(
            "pk",
            "categoryType",
            "boardAnimalTypes",
            "user",
            "content",
            "Image",#ImageModel의 related_name 이용 
            "likeCount",
            "likeCheck",
        )

    def get_likeCheck(self, data):
        request=self.context.get("request")
        if request and request.user.is_authenticated:
            return PostLike.objects.filter(user=request.user, post=data).exists()
        return False

    
    def create(self, validated_data):  
        
        category_data=validated_data.pop("categoryType", None)
        print("category_data: ", category_data)
        pet_category_data=validated_data.pop("boardAnimalTypes", None)
        print("pet_: ", pet_category_data)
        image_data = validated_data.pop("Image", None)#값 없으면 None
        try:
            with transaction.atomic():
                post = Post.objects.create(**validated_data)
                if category_data:
                    for i in Category.objects.all():
                        print(i.categoryType)
                    categoryType=Category.objects.filter(categoryType=category_data).first()
                    post.categoryType=categoryType
                    post.save()

                if image_data:
                    if isinstance(image_data, list):
                        if len(image_data)<=5:
                            for img in image_data:
                                Image.objects.create(post=post, img_path=img.get("img_path"))
                        else:
                            raise ParseError("이미지는 최대 5장 까지 업로드 할 수 있습니다.") 
                    else:
                        raise ParseError("image 잘못된 형식 입니다.")               

                if pet_category_data:
                    if isinstance(pet_category_data, list):
                        for pet_category in pet_category_data:
                            pet_category = get_object_or_404(Pet,animalTypes=pet_category)
                            post.boardAnimalTypes.add(pet_category)
                    else:
                        pet_category = get_object_or_404(Pet, animalTypes=pet_category_data)
                        post.boardAnimalTypes.add(pet_category)
                else:
                    raise ParseError({"error": "잘못된 형식입니다."})
        
        except Exception as e:
            raise ValidationError({"error":str(e)})
        return post
        
    def validate(self, data):
        content = data.get('content', None)
        images = data.get('Image', None)
        if content is None and images is None:
            raise ParseError({"error": "내용을 입력해주세요."})
        if images and len(images)>5:
            raise ParseError({"error":"이미지는 최대 5개까지 등록이 가능합니다."})
        return data

class PostListSerializers(ModelSerializer):#간략한 정보만을 보여줌
    user=TinyUserSerializers(read_only=True)
    boardAnimalTypes=PetsSerializers(many=True)
    categoryType=BoardSerializers()
    Image=ImageSerializers(many=True, read_only=True, required=False)
    commentCount=serializers.SerializerMethodField()
    class Meta:
        model=Post
        fields=(
            "pk",
            "categoryType",
            "boardAnimalTypes",
            "user",
            "content",
            "Image",
            "createdDate", 
            "updatedDate",
            "viewCount",#조회수
            "likeCount",#좋아요 수 
            "commentCount",#댓글 수 (대댓글 미포함)
            "bookmarkCount",#북마크 수
        )
    def get_images(self, post):
        images = post.images.all()
        if images.exists():
            return ImageSerializers(images.first(), context=self.context).data   
        return [] 
    def get_commentCount(self, obj):
        return obj.commentCount
    
     
class PostDetailSerializers(ModelSerializer):#image 나열
    user=TinyUserSerializers()
    boardAnimalTypes=PetsSerializers(many=True)
    categoryType=BoardSerializers()
    Image=ImageSerializers(many=True, read_only=True, required=False)
    likeCheck=serializers.SerializerMethodField()
    commentCount=serializers.SerializerMethodField()
    bookmarkCheck=serializers.SerializerMethodField()
    class Meta:
        model=Post
        fields=(
            "id",
            "categoryType",
            "boardAnimalTypes",
            "user", 
            "content",
            "Image",
            "createdDate",
            "updatedDate",    
            "viewCount",# 조회수 
            "likeCount",# 좋아요 수
            "likeCheck",#좋아요 토글
            "commentCount",#댓글 수 
            "bookmarkCheck",#북마크 토글
            "bookmarkCount",#북마크 수
        )
    
    def get_likeCheck(self, data):
        request = self.context.get("request")
        if request:
            if request.user.is_authenticated:
                return PostLike.objects.filter(user=request.user,post__pk=data.pk).exists()
        return False
    
    def get_commentCount(self, obj):
        return obj.commentCount
    
    def get_bookmarkCheck(self, data):
        request=self.context.get("request")
        if request and request.user.is_authenticated:
            return Bookmark.objects.filter(user=request.user, post=data).exists()
        return False
    
    #{ update()-put()
    #"content": "test",
    #"categoryType": {"categoryType": "반려고수"},
    #"boardAnimalTypes": [{"animalTypes": "강아지"}, {"animalTypes":"햄스터"}, {"animalTypes":"기타"}]
    #}
    # image : 다중 이미지 만들기. 
    def update(self, instance, validated_data):
        
        instance.boardAnimalTypes.clear()
        pet_category_data = validated_data.pop("boardAnimalTypes", None)
        category_data = validated_data.pop("categoryType", None)
        
        # image_data = validated_data.pop("Image", None)
  
        if category_data:
            category_instance = Category.objects.filter(categoryType=category_data.get("categoryType")).first()
            if not category_instance:
                raise serializers.ValidationError({"category": "Invalid category"})
            instance.categoryType = category_instance

        # Update the remaining fields
        instance = super().update(instance, validated_data)

        # Update the many-to-many fields
        if pet_category_data is not None:
            for pet_category in pet_category_data:
                animalTypes = pet_category.get("animalTypes")
                if animalTypes:
                    pet_category, _ = Pet.objects.get_or_create(animalTypes=animalTypes)
                    instance.boardAnimalTypes.add(pet_category)
        
        # if image_data is not None:
        #     for i, image in enumerate(image_data):
        #         Image.objects.update_or_create(id=image.get("id"), defaults={"image": image.get("image"), "order": i, "post": instance})            
        
        instance.save()
        return instance
  