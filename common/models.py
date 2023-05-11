from django.db import models

class CommonModel(models.Model):

    createdDate = models.DateTimeField(
        auto_now_add=True,
    ) 
    updatedDate = models.DateTimeField(
        auto_now=True,
    )  
    class Meta: 
        abstract = True
