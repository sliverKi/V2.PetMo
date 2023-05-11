from django.db import models
from common.models import CommonModel

class Bookmark(CommonModel):

    user=models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="bookmarks"
    )
    post=models.ForeignKey(
        "posts.Post",
        on_delete=models.CASCADE,
        related_name="bookmarks"
    )
    mark=models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user} - {self.post}"