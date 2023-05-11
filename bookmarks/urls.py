from django.urls import path
from . import views

urlpatterns=[
    path("", views.Bookmarks.as_view()),
    path("<int:pk>", views.MarkDetail.as_view()),
    
]

#+) bookmakrCount 추가하기