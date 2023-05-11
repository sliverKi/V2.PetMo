from django.contrib import admin
from django.urls import path
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views 

urlpatterns=[
    path("sign-up", views.Register.as_view(), name="register"),
    path("sign-in", views.LogIn.as_view(), name="login"),
    path("sign-out", views.LogOut.as_view(), name="logout"),

    path("kakao", views.KakaoLogin.as_view(), name="socialLogin by Kakao"),
    path("kakao/callback", views.KakaoCallBack.as_view()),

    path("naver", views.NaverLogin.as_view(), name="socialLogin by Naver"),
    # path("naver/callback", views.NaverCallBack.as_view()),
    # path("sign-in/refresh", views.TokenBlack.as_view(), name="get_newToken"),
]