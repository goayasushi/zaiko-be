from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import UserInfoView

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("info/", UserInfoView.as_view(), name="user_info"),
]
