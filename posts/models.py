from django.db import models

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
        max_length=550,
        blank=True,
        null=True,
    )
    boardAnimalTypes=models.ManyToManyField(
        "pets.Pet",
        related_name="posts",
        null=True,
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
        on_delete=models.CASCADE,
        help_text="댓글 작성자의 pk"
    )    
    post=models.ForeignKey(
        "posts.Post",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="post_comments",
        help_text="댓글이 달린 게시글의 pk"
    )
    content=models.CharField(#댓글 작성
        max_length=150,
        blank=True,
        null=True,
        help_text="댓글 내용"
    )
    parent_comment=models.ForeignKey(#parent_comment에 값이 있으면 대댓글, 값이 없으면 댓글 
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="replies",
        help_text="댓글 인지 대댓글인지 구분 토글, if parent_comment==Null: 댓글, else: 대댓글"
    )
   
    def __str__(self):
        return f"{self.user} - {self.content}"
    