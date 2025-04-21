"""
URL configuration for zaiko_be project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import debug_toolbar


# ヘルスチェック用のビュー関数
@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    """
    ALBのヘルスチェック用エンドポイント
    認証なしでアクセス可能で、サービスの稼働状態を返す
    """
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/masters/", include("masters.urls")),
    path("health/", health_check, name="health_check"),  # ヘルスチェック用URLパターン
    path("api-auth/", include("rest_framework.urls")),
    path("__debug__/", include(debug_toolbar.urls)),
]
