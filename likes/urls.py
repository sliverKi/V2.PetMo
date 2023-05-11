
from django.urls import path
from . import views

urlpatterns=[
    path("post/<int:pk>", views.PostLikes.as_view())
]