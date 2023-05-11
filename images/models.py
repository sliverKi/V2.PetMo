from django.db import models
from common.models import CommonModel

class Image(CommonModel):
    post=models.ForeignKey(
        "posts.Post",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="Image"
    )
    img_path=models.URLField()
