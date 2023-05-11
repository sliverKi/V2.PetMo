from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PostLike
from posts.models import Post


class PostLikes(APIView):    
    def post(self, request, pk):
        #input data: {"post":1}
        post = get_object_or_404(Post, pk=pk)#pk에 해당하는 Post 객체를 가져옴. 
        like, created = PostLike.objects.get_or_create(
            user=request.user, 
            post=post
        )
        #현재 사용자와, 게시글에 대한 좋아요 객체가 이미 존재하는 경우, 해당 객체를 가져오고 없는 경우 새로운 객체를 생성함.
        #get_or_create:: 생성 여부를 boolean 으로 반환
        like.delete() if not created else None
        return Response({"created" if created else "deleted"}, status=status.HTTP_200_OK)

