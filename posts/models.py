from django.db import models
from django.db.models import Count
from common.models import CommonModel


# 해야 할일 -> 다중이미지,
# 댓글 pageniation 최대 5개까지 보여주기
# 대댓글 3개
# 좋아요, 조회수, 댓글수, 북마크 수
class Post(CommonModel):
    user=models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="posts"
    )
    content=models.TextField(
        max_length=255,
        blank=True,
        null=True,
    )
    boardAnimalTypes=models.ManyToManyField(
        "pets.Pet",
        related_name="posts"
    )
    categoryType=models.ForeignKey(
        "categories.Category",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="posts",
    )
    viewCount=models.PositiveIntegerField( # 조회수
        default=0,
        editable=False,
    )

    @property
    def likeCount(self):
        return self.postlike.count()
    
    @property
    def commentCount(self):
        return self.post_comments.filter(parent_comment=None).count()
    
    @property
    def bookmarkCount(self):
        return self.bookmarks.count()
    
    def __str__(self):
        return f"{self.user} - {self.content}"
    


class Comment(CommonModel):
    user=models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE
    )    
    post=models.ForeignKey(
        "posts.Post",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="post_comments",
    )
    content=models.CharField(#댓글 작성
        max_length=150,
        blank=True,
        null=True,
    )
    parent_comment=models.ForeignKey(#parent_comment에 값이 있으면 대댓글, 값이 없으면 댓글 
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="replies",
    )
   
    def __str__(self):
        return f"{self.user} - {self.content}"
    