from django.urls import path, include
from rest_framework.routers import DefaultRouter
from masters.views import SupplierViewSet

# DRFのルーターを設定
router = DefaultRouter()
router.register(r"suppliers", SupplierViewSet, basename="supplier")

# 将来的に他のマスタモデルも追加可能

urlpatterns = [
    path("", include(router.urls)),
]
